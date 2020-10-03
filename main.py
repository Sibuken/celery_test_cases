from typing import Generator, AsyncGenerator, NoReturn
import wave
import math
import asyncio
import requests
import io
import struct
import subprocess


def get_request(url: str) -> requests.Response:
    return requests.get(url, timeout=3)


def create_generator() -> Generator[int]:
    for i in range(10):
        yield i * i


async def async_create_generator() -> AsyncGenerator[int]:
    for i in range(10):
        yield i * i
        await asyncio.sleep(0.1)


async def read_from_async_gen() -> int:
    s = 0
    async for i in async_create_generator():
        s += i

    return s


def subprocess_task() -> NoReturn:
    command = "ls"

    process_handle = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    process_handle.communicate()
    status = process_handle.returncode

    assert not status


def create_audio_wave_task() -> NoReturn:
    sample_rate = 44100.0
    duration = 500
    nchannels = 1
    sampwidth = 2

    comptype = "NONE"
    compname = "not compressed"

    volume = 1.0
    freq = 440.0
    audio = []
    num_samples = duration * (sample_rate / 1000.0)
    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * (x / sample_rate)))

    nframes = len(audio)

    ok: bool = True
    try:
        with io.BytesIO() as buf:
            with wave.open(buf, "w") as wav_file:
                wav_file.setparams(
                    (nchannels, sampwidth, sample_rate, nframes, comptype, compname)
                )
                for sample in audio:
                    wav_file.writeframes(struct.pack("h", int(sample * 32767.0)))

            buf.seek(0)
    except Exception as er:
        print(er)
        ok = False

    assert ok


def async_task() -> NoReturn:
    async def coro() -> int:
        await asyncio.sleep(1)
        return 1

    res = asyncio.run(coro())

    assert res == 1


def request_task() -> NoReturn:
    url = "https://google.com/"

    try:
        resp = get_request(url)
        code = resp.status_code
    except requests.RequestException:
        code = 500

    assert 500 > code


def yield_task() -> NoReturn:
    assert 285 == sum(create_generator())


def async_yield_task() -> NoReturn:
    res = asyncio.run(read_from_async_gen())
    assert 285 == res


if __name__ == '__main__':
    subprocess_task()
    create_audio_wave_task()
    async_task()
    request_task()
    yield_task()
    async_yield_task()
