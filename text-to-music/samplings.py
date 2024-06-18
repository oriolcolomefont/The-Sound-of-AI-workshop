"""
Samplings
=========

A collection of sampling methods for machine learning implemented on numpy.

Author: Sander Wood

Provides
  1. Gamma sampling for controllable generation
  2. Local temperature sampling with weights
  3. Nucleus sampling (top-p sampling)
  4. Top-k sampling
  5. Random sampling

How to use
----------
As you probably know, sampling means randomly picking the next token according 
to its conditional probability distribution. In other words, given the same 
probability distribution, you may get a different result each time. If you 
want to get rid of this uncertainty, you can set `seed` to a fixed value.

By default, all the functions in `samplings` return the index of the next token.
However, you can ask them to return the modified probability distribution by set 
`return_probs` as `True`. Then, you can make further manipulations based on this 
probability distribution.

In addition to the probability distribution, most sampling methods require other
parameters for modifying the probability distribution to achieve desired results.
Please refer to the docstring of each function for details.

About gamma sampling
----------------------
Gamma sampling is a method of tuning probabilities of target tokens to achieve 
controlling specific properties of the generated sequence. The basic assumption is 
that some attributes of sequences are closely related to the frequencies of some tokens. 
As long as the controllable attribute can be defined at the token level, prior knowledge 
can be directly brought into the sampling process, allowing arbitrary models to support 
customisable and controllable generation.
"""

import numpy as np

np.seterr(divide='ignore')

def build_mask(len_probs, tokens):
    """            
    Generates a mask from the given indices of tokens.

    # Parameters

        len_probs (`int`):
            The length of the next token probability distribution.
        tokens (`array_like`):
            Indices of tokens need to be masked.
    
    # Returns

        mask (`ndarray`): 
            A boolean array with the length of `len_probs` where indices given in `tokens` are `True`.

    # Examples

        >>> from samplings import build_mask
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> tokens = [0, 3]
        >>> build_mask(len_probs=len(probs), tokens=tokens)
        [ True False False  True]
    """
    
    # Initialising the mask
    mask = np.zeros(len_probs).astype(bool)

    # Set masked tokens
    if len(tokens)!=0:
        mask[tokens] = True
    
    return mask


def random_sampling(probs, seed=None):
    """            
    Selects a random index from the given probability distribution.
    
    # Parameters

        probs (`array_like`):
            The probability distribution.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.

    # Returns

        index (`int`): 
            The randomly sampled index of the next token from `probs`.

    # Tips

        For reproducibility, you can set `seed` to an integer.
    
    # Examples

        >>> from samplings import random_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> random_sampling(probs=probs, seed=0)
        2
    """

    # Set seed
    if seed!=None:
        np.random.seed(seed)

    return np.random.choice(range(len(probs)), p=probs)


def top_k_sampling(probs,
                   top_k,
                   seed=None,
                   return_probs=False):
    """            
    Sorting by probability and zeroing out the probabilities for anything below the k-th token.

    # Parameters

        probs (`array_like`):
            The probability distribution.
        top_k (`int`):
            The positive integer of highest probabilities vocabulary tokens to keep for top-k-filtering.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.
    
    # Returns

        index (`int`):
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n
    
    # Examples

        >>> from samplings import top_k_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> top_k_sampling(probs=probs, 
                           top_k=2,
                           return_probs=True)
        [0.         0.         0.42857143 0.57142857]
        >>> top_k_sampling(probs=probs, 
                           top_k=3,
                           return_probs=True)
        [0.         0.22222222 0.33333333 0.44444444]

    # References
        - Angela Fan, Mike Lewis, Yann N. Dauphin:
        ["Hierarchical Neural Story Generation"](https://arxiv.org/pdf/1805.04833.pdf). ACL (1) 2018: 889-898
    """

    if top_k>0:
        # Sort probability distribution
        sorted_tokens = np.argsort(probs)[::-1]
        sorted_tokens_to_remove = [0]*top_k+[1]*(len(probs)-top_k)
        tokens_to_remove = sorted_tokens[np.array(sorted_tokens_to_remove).astype(bool)]
        
        # Remove tokens with small probabilities
        mask = build_mask(len(probs), tokens_to_remove)
        probs = np.ma.array(probs, mask=~mask)
        probs -= probs
        probs = np.array(probs)
        probs /= probs.sum()

    # Return probability distribution
    if return_probs:
        return probs
    
    # Return index
    else:
        return random_sampling(probs, seed=seed)


def top_p_sampling(probs,
                   top_p,
                   seed=None,
                   return_probs=False):
    """            
    Also known as nucleus sampling, which shortlists the top tokens whose sum of likelihoods does not exceed a certain value. 
    
    # Parameters

        probs (`array_like`):
            The probability distribution.
        top_p (`float`):
            A positive decimal which not greater than 1.
            Only the most possible tokens with probabilities that add up to 
            `top_p` or higher are kept for generation.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.

    # Returns

        index (`int`)
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n

    # Examples
    
        >>> from samplings import top_p_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> top_p_sampling(probs=probs, 
                           top_p=0.5,
                           return_probs=True)
        [0.         0.         0.42857143 0.57142857]
        >>> top_p_sampling(probs=probs, 
                           top_p=0.7,
                           return_probs=True)
        [0.         0.22222222 0.33333333 0.44444444]

    # References

        - Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi: 
        ["The Curious Case of Neural Text Degeneration"](https://arxiv.org/pdf/1904.09751.pdf). ICLR 2020
    """

    if 0<top_p and top_p<1:
        # Sort probability distribution
        sorted_probs = np.sort(probs)[::-1]
        sorted_tokens = np.argsort(probs)[::-1]
        cumulative_probs = np.cumsum(sorted_probs)
        sorted_tokens_to_remove = cumulative_probs > top_p

        # Logical right shift
        sorted_tokens_to_remove[1:] = sorted_tokens_to_remove[:-1]
        sorted_tokens_to_remove[0] = 0

        # Remove tokens with small probabilities
        tokens_to_remove = sorted_tokens[sorted_tokens_to_remove]
        mask = build_mask(len(probs), tokens_to_remove)
        probs = np.ma.array(probs, mask=~mask)
        probs -= probs
        probs = np.array(probs)
        probs /= probs.sum()

    # Return probability distribution
    if return_probs:
        return probs
    
    # Return index
    else:
        return random_sampling(probs, seed=seed)


def temperature_sampling(probs,
                         temperature,
                         weights=1,
                         tempered_tokens=[],
                         seed=None,
                         return_probs=False):
    """            
    Lower temperatures (< 1) make the model increasingly confident in its top choices and vice versa.

    If you want to use penalized sampling, please set `weights` to an array with the same length of `probs`.

    If only some of the tokens' probabilities are intended to be changed, you can specify their indices by setting `tempered_tokens`.

    # Parameters

        probs (`array_like`):
            The probability distribution.
        temperature (`float`):
            A non-negative number which used to module the sharpness of the probability distribution.
        weights (`array_like`, *optional*, defaults to `1`):
            An array of probability weights for temperature sampling with the same length of `probs`.
        tempered_tokens (`array_like`, *optional*, defaults to `[]`):
            A list of indices of tokens need to be tempered, the rest tokens' probabilities will keep intact.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.
    
    # Returns

        index (`int`):
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n
    
    # Examples

        >>> from samplings import temperature_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> weights = [1.2, 1.2, 1, 1]
        >>> tempered_tokens = [0, 1]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 return_probs=True)
        [0.03333333 0.13333333 0.3        0.53333333]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 weights=weights,
                                 return_probs=True)
        [0.01447698 0.07640994 0.32728071 0.58183237]
        >>> temperature_sampling(probs=probs, 
                                 temperature=0.5,
                                 tempered_tokens=tempered_tokens,
                                 return_probs=True)
        [0.06 0.24 0.3  0.4 ]

    # References

        - David H. Ackley, Geoffrey E. Hinton, Terrence J. Sejnowski: 
        ["A Learning Algorithm for Boltzmann Machines"](https://onlinelibrary.wiley.com/doi/pdfdirect/10.1207/s15516709cog0901_7). Cogn. Sci. 9(1): 147-169 (1985)

        - Nitish Shirish Keskar, Bryan McCann, Lav R. Varshney, Caiming Xiong, Richard Socher: 
        ["CTRL: A Conditional Transformer Language Model for Controllable Generation"](https://arxiv.org/pdf/1909.05858.pdf). CoRR abs/1909.05858 (2019)
    """

    if temperature != 1:
        # Mask modified tokens
        if len(tempered_tokens)==0:
            tempered_tokens = range(len(probs))

        modified_mask = build_mask(len(probs), tempered_tokens)
        modified_sum = np.dot(probs, modified_mask)

        # Divide log probability by the temperature before softmax
        probs = np.where(modified_mask, probs/modified_sum, probs)
        probs = np.where(modified_mask, np.log(probs)*np.array(weights)/temperature, probs)
        probs = np.where(modified_mask, modified_sum*np.exp(probs)/np.sum(np.where(modified_mask, np.exp(probs), 0)), probs)
        
    # Return probability distribution
    if return_probs:
        return probs
    
    # Return index
    else:
        return random_sampling(probs, seed=seed)


def gamma_sampling(probs,
                   tokens_list,
                   gamma_list,
                   activation='tan',
                   top_k=0,
                   top_p=1.0,
                   temperature=1.0,
                   weights=1,
                   tempered_tokens=[],
                   seed=None,
                   return_probs=False):
    """            
    Increase or decrease probabilities of target tokens (specified by `tokens_list`) to achieve controllable generation. 

    However, if you set gamma too small, some target tokens with noise probabilities would dramatically increase to values that are not acceptable.

    You can get around this problem by set `top_k` > 0 or set `top_p` < 1 when calling gamma sampling.

    # Parameters

        probs (`array_like`):
            The probability distribution.
        tokens_list (`array_like`):
            A two-dimensional list whose elements are lists of indices of target tokens.
            Those target tokens can define some attributes of generated sequences.
        gamma_list (`array_like`):
            A one-dimensional list with the same length of `token_list`.
            Each element is a gamma parameter within a range of 0 to 1.
        activation (`str`, *optional*, defaults to `tan`):
            Activation function to use.
        top_k (`int`, *optional*, defaults to `0`):
            The positive integer of highest probabilities vocabulary tokens to keep for top-k-filtering.
        top_p (`float`, *optional*, defaults to `1.0`):
            A positive decimal which not greater than 1.
            Only the most possible tokens with probabilities that add up to 
            `top_p` or higher are kept for generation.
        temperature (`float`, *optional*, defaults to `1.0`):
            A non-negative number which used to module the sharpness of the probability distribution.
        weights (`array_like`, *optional*, defaults to `1`):
            An array of probability weights for temperature sampling with the same length of `probs`.
        tempered_tokens (`array_like`, *optional*, defaults to `[]`):
            A list of indices of tokens need to be tempered, the rest tokens' probabilities will keep intact.
        seed (`int`, *optional*, defaults to `None`):
            Seed for RandomState. Must be convertible to 32-bit unsigned integers.
        return_probs (`bool`, *optional*, defaults to `False`):
            Whether or not to return the modified probability distribution. 
            If set to `False`, return the randomly sampled index.

    # Available activations

    Here x is the sum of target tokens probabilities, g is gamma.

    ## tan

        Default activation: `f(x) = x^tan(pi*g/2)`. When d < 0.5, increase x and vice versa.

    ## log

        Gatekeeper activation: `f(x) = x^(log(2)/log(1/g))`. Same as the default one, but gamma is also the probability threshold.

    ## frac

        Reduction activation: `f(x) = x^(1/g)`. Only decrease x.

    ## linear

        Amplification activation: `f(x) = x^g`. Only increase x.
    
    # Returns

        index (`int`):
            The randomly sampled index of the next token from modified `probs` (when `return_probs` is `False`).
        probs (`ndarray`):
            The modified probability distribution (when `return_probs` is `True`).

    # Tips

        For reproducibility, you can set `seed` to an integer.\n
        When used with `return_probs=True`, you can get the modified probability distribution.\n
        Then, you can make further manipulations based on this probability distribution.\n

    # Examples

        >>> from samplings import gamma_sampling
        >>> probs = [0.1, 0.2, 0.3, 0.4]
        >>> gamma_sampling(probs=probs, 
                           tokens_list=[[0, 1]], 
                           gamma_list=[0.1], 
                           return_probs=True)
        [0.27546276 0.55092551 0.07440503 0.0992067 ]
        >>> gamma_sampling(probs=probs, 
                           tokens_list=[[0, 1]], 
                           gamma_list=[0.9], 
                           return_probs=True)
        [1.66552929e-04 3.33105859e-04 4.28357289e-01 5.71143052e-01]
    
    # References

        - Shangda Wu, Maosong Sun: 
        ["Gamma Sampling: Fine-grained Controlling Language Models without training"](https://arxiv.org/pdf/2205.06036.pdf)
    """

    # Pre-sampling
    probs = top_k_sampling(probs=probs, 
                           top_k=top_k, 
                           return_probs=True)
    probs = top_p_sampling(probs=probs, 
                           top_p=top_p, 
                           return_probs=True)

    # Initialise frozen tokens
    frozen_tokens = []
    frozen_sum = 0

    # Travers all densities
    for idx, gamma in enumerate(gamma_list):

        # Initialise target tokens
        modified_tokens = tokens_list[idx]
        modified_mask = build_mask(len(probs), modified_tokens)
        modified_sum = np.dot(probs, modified_mask)

        # Remove target tokens from frozen tokens
        remodified_tokens = list(set(frozen_tokens).intersection(set(modified_tokens)))
        remodified_mask = build_mask(len(probs), remodified_tokens)

        frozen_tokens = list(set(frozen_tokens).difference(set(modified_tokens)))
        frozen_mask = build_mask(len(probs), frozen_tokens)
        frozen_sum -= np.dot(probs, remodified_mask)

        # Skip extreme cases
        if np.isclose(modified_sum, 0, rtol=0, atol=1e-06) or \
           np.isclose(modified_sum, 1, rtol=0, atol=1e-06):
            continue
        
        # Save sums
        rest_sum = 1-modified_sum-frozen_sum
        original_sum = modified_sum

        # Caculate the new probabilities of target tokens based on the selected activation
        if gamma != 0.5:
            modified_sum /= (1-frozen_sum)

            if activation=='tan':
                modified_sum **= (np.tan(np.pi*gamma/2))

            elif activation=='log':
                modified_sum **= (np.log(2)/np.log(1/gamma))

            elif activation=='frac':
                modified_sum **= (1/gamma)

            elif activation=='linear':
                modified_sum **= gamma
            
            modified_sum *= (1-frozen_sum)

        # Update target tokens
        probs = np.ma.array(probs, mask=~modified_mask)
        probs *= (modified_sum/original_sum)
        probs = np.array(probs)
        
        # Update frozen tokens
        frozen_sum += modified_sum
        frozen_tokens += modified_tokens

        # Normolise rest tokens
        frozen_mask += modified_mask
        probs = np.ma.array(probs, mask=frozen_mask)
        probs += (original_sum-modified_sum)*(probs/rest_sum)
        probs = np.array(probs)
        
        # Filter illegal values
        probs = np.where(np.isnan(probs), 0, probs)
        probs = np.where(0<=probs, probs, 0)
        probs = np.where(probs<=1, probs, 1)
        probs /= probs.sum()
    
    # Post-sampling
    probs = temperature_sampling(probs=probs, 
                                 temperature=temperature, 
                                 weights=weights,
                                 tempered_tokens=tempered_tokens,
                                 return_probs=True)

    # Return probability distribution
    if return_probs:
        return probs
    
    # Return index
    else:
        return random_sampling(probs=probs, seed=seed)