#!/usr/bin/env python3
"""Transform an Electronic Frontier Foundation (EFF) wordlist file into JSON."""
import io
import os
import json
import typing as ty
import argparse
import urllib.parse
import urllib.request

from types import TracebackType
from pathlib import Path


PROG_NAME = "wordlist2json.py"
PROG_DESC = "Transform an EFF wordlist file into JSON."

DEFAULT_TIMEOUT = 15
EFF_WORDLIST_URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"


class EFFWordlist(object):
    """Context manager and iterable for loading EFF wordlist files.

    Provides streaming access to dice roll sequences and words loaded either
    from a local filesystem path or a remote URL.

    """

    def __init__(
        self,
        url: str | urllib.parse.SplitResult | None = None,
        path: str | os.PathLike[str] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the EFF wordlist source.

        :param url: URL pointing to an EFF wordlist file.
        :type url: str | ~urllib.parse.SplitResult | None

        :param path: Filesystem path to an EFF wordlist file.
        :type path: str | ~os.PathLike[str] | None

        :param timeout: Network timeout in seconds when streaming from a URL.
        :type timeout: int


        :raises ValueError: If neither *url* nor *path* is provided.

        """
        if not (url or path):
            raise ValueError("One of `url` or `path` is required.")

        self.fp = None
        if path:
            self.source = Path(path)
        elif isinstance(url, urllib.parse.SplitResult):
            self.source = url
        elif url:
            self.source = urllib.parse.urlsplit(url)
        else:
            self.source = None

        self.timeout = timeout

    def __enter__(self) -> io.TextIOBase:
        """Open the wordlist source and return an active text stream.

        :return: An open text stream ready for reading.
        :rtype: ~io.TextIOBase


        :raises ValueError: If no valid source is configured.

        """
        if isinstance(self.source, Path):
            self.fp = self.source.open("r")
        elif isinstance(self.source, urllib.parse.SplitResult):
            self.fp = from_url(self.source, timeout=self.timeout)
        else:
            raise ValueError("No source available.")
        return self.fp

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Close the active text stream upon exiting the context.

        :param exc_type: The exception type, if an exception occurred.
        :type exc_type: ~type[BaseException] | None

        :param exc_val: The exception instance, if an exception occurred.
        :type exc_val: ~BaseException | None

        :param exc_tb: The traceback object, if an exception occurred.
        :type exc_tb: ~types.TracebackType | None

        """
        if self.fp is not None:
            self.fp.close()
            self.fp = None

    def __iter__(self) -> ty.Iterator[tuple[str, str]]:
        """Iterate over the wordlist, yielding sequence and word pairs.

        Lines starting with ``#`` and empty lines are skipped.


        :return: An iterator yielding tuples of ``(sequence, word)``.
        :rtype: ~typing.Iterator[tuple[str, str]]

        """
        with self as fp:
            for line in filter(None, map(str.strip, fp)):
                if line.startswith("#"):
                    continue
                sequence, word = map(str.strip, line.split(maxsplit=1))
                yield sequence, word

    @staticmethod
    def word_to_dict(
        root: ty.MutableMapping[str, ty.Any],
        sequence: str,
        word: str,
        nested: bool = False,
    ) -> None:
        """Insert a dice sequence and word pair into the target mapping.

        If *flat* is ``True``, the sequence is mapped directly to the word.
        Otherwise, intermediate digits in the sequence are nested as dictionary
        keys.


        :param root: The root mapping to populate.
        :type root: ~typing.MutableMapping[str, ~typing.Any]

        :param sequence: The dice roll sequence (e.g. ``"11111"``).
        :type sequence: str

        :param word: The word associated with the dice sequence.
        :type word: str

        :param nested: Whether to generate a nested mapping where each item in
                       the sequence diverts to a new dictionary.
        :type nested: bool

        """
        if nested:
            curr = root
            for x in sequence[:-1]:
                curr = curr.setdefault(x, {})
            curr[sequence[-1]] = word
        else:
            root[sequence] = word


def from_url(
    url: str | urllib.parse.SplitResult, timeout: int = DEFAULT_TIMEOUT
) -> io.TextIOWrapper:
    """Stream a wordlist file directly from a remote URL.

    :param url: The URL to fetch the wordlist from.
    :type url: str | ~urllib.parse.SplitResult

    :param timeout: Network timeout in seconds.
    :type timeout: int


    :return: A text stream wrapping the HTTP response socket.
    :rtype: ~io.TextIOWrapper

    """
    target = (
        urllib.parse.urlunsplit(url)
        if isinstance(url, urllib.parse.SplitResult)
        else url
    )
    response = urllib.request.urlopen(target, timeout=timeout)
    return io.TextIOWrapper(response)


def parse_args(args: ty.Sequence[str] | None = None) -> argparse.Namespace:
    """Parse and validate command-line arguments.

    :param args: Sequence of argument strings to parse, or ``None`` to use
                 standard arguments from :data:`sys.argv`.
    :type args: ~typing.Sequence[str] | None


    :return: The parsed command-line argument namespace.
    :rtype: ~argparse.Namespace

    """
    parser = argparse.ArgumentParser(prog=PROG_NAME, description=PROG_DESC)

    parser.add_argument(
        "output",
        metavar="OUTPUT",
        type=Path,
        help="path to the generated JSON file",
    )

    src = parser.add_mutually_exclusive_group()
    src.add_argument(
        "-U",
        "--url",
        default=EFF_WORDLIST_URL,
        type=urllib.parse.urlsplit,
        help="URL to an EFF wordlist file",
    )

    src.add_argument(
        "-F",
        "--file",
        type=Path,
        help="path to an EFF wordlist file",
    )

    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        default=None,
        help="indentation level for the generated JSON file",
    )

    parser.add_argument(
        "-s",
        "--sort",
        action="store_true",
        default=False,
        help="sort the generated JSON file",
    )

    parser.add_argument(
        "-w",
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="timeout in seconds for the URL request",
    )

    parser.add_argument(
        "-x",
        "--extend",
        action="store_true",
        default=False,
        help="generate a nested JSON structure",
    )

    return parser.parse_args(args)


def main():
    """Parse CLI arguments and transform the EFF wordlist into JSON."""
    opts = parse_args()

    output = {}

    wordlist = EFFWordlist(url=opts.url, path=opts.file, timeout=opts.timeout)
    for sequence, word in wordlist:
        wordlist.word_to_dict(output, sequence, word, nested=opts.extend)

    opts.output.parent.mkdir(parents=True, exist_ok=True)
    with opts.output.open("w") as fp:
        json.dump(output, fp, indent=opts.indent, sort_keys=opts.sort)


if __name__ == "__main__":
    main()
