from __future__ import annotations
from typing import Iterator


def transform(subject_number: int) -> Iterator[int]:
    value = 1
    while True:
        value = value * subject_number
        value = value % 20201227
        yield value


def find_private_key(subject_number: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = value * subject_number
        value = value % 20201227
    return value


"""
The card transforms the subject number of the door's public key according to the card's loop size. 
The result is the encryption key.

The door transforms the subject number of the card's public key according to the door's loop size. 
The result is the same encryption key as the card calculated.
"""


def find_loop_size(target: int, subject_number: int) -> int:
    counter = 1
    transformer = transform(subject_number)
    while next(transformer) != target:
        counter += 1
    return counter


## Unit test:
card_public_key = 5764801
door_public_key = 17807724


card_loop = find_loop_size(card_public_key, 7)
door_loop = find_loop_size(door_public_key, 7)


print(card_loop, door_loop)
print(find_private_key(door_public_key, card_loop))
print(find_private_key(card_public_key, door_loop))

## Problem
card_public_key = 9232416
door_public_key = 14144084


card_loop = find_loop_size(card_public_key, 7)
door_loop = find_loop_size(door_public_key, 7)


print(card_loop, door_loop)
print(find_private_key(door_public_key, card_loop))
print(find_private_key(card_public_key, door_loop))
