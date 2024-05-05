import random


def read_audio_samples(buffer_size):
    # Generate random audio samples
    samples = [random.randint(-2 ** 31, 2 ** 31 - 1) for _ in range(buffer_size)]
    return samples


# Example usage
buffer_size = 512

samples = read_audio_samples(buffer_size)
print(samples)
