import time
import modules
import discord
import functools
import typing as t
from modules import constants
from os import path as os_path
from operator import attrgetter


__all__ = [
    "log",
    "get",
    "find",
    "is_exists",
    "has_ayn_role",
    "create_embed",
    "strftime_translate"
]

T = t.TypeVar("T")


def is_exists(path: str) -> bool:
    """
        Check if path exists.

        :param path: The path to check.
        :type path: str
        :rtype: bool
    """
    return os_path.exists(path)


def log(msg: str, level: str = "info"):
    """
        Print log.

        :param level: Log level.
        :param msg: Log message.
        :type level: str
        :type msg: str
    """
    levels = {"info": "[INFO]", "warning": "[WARNING]", "error": "[ERROR]", "dev": "[DEVELOP]"}
    
    print(f"{time.strftime('%d.%m.%YT%H:%M:%S')} :: {levels[level]} {msg}")


def find(predicate: t.Callable[[T], t.Any], seq: t.Iterable[T], only_first = False) -> t.Union[T, list[T]] | None:
    """
        Return the elements found in the sequence that meets the predicate.
        If an entry is not found, then ``None`` is returned.

         Examples
        ---------

        Basic usage:

        .. code-block:: python3

            member = find(lambda m: m.name == 'Mighty', [m])

        :param predicate: A function that returns a boolean-like result.
        :param seq: The iterable to search through.
        :param only_first: Retuens only fisrt element.
        :type predicate: Callable
        :type seq: Iterable
        :type only_first: bool
    """
    elements = []

    for element in seq:
        if predicate(element):
            elements.append(element)
    
    if only_first and len(elements) > 0:
        return elements[0]
    
    if len(elements) == 1:
        return elements[0]
    elif len(elements) > 1:
        return elements
    return None


def get(iterable: t.Iterable[T], **attrs: t.Any) -> t.Union[T, t.List[T], None]:
    r"""
        A helper that returns the elements in the iterable that meets
        all the traits passed in ``attrs``. 

        When multiple attributes are specified, they are checked using
        logical AND, not logical OR. Meaning they have to meet every
        attribute passed in and not one of them.

        To have a nested attribute search (i.e. search by ``x.y``) then
        pass in ``x__y`` as the keyword argument.

        If nothing is found that matches the attributes passed, then
        ``None`` is returned.

        Examples
        ---------

        Basic usage:

        .. code-block:: python3

            member = modules.get(message.guild.members, name='Foo')

        Multiple attribute matching:

        .. code-block:: python3

            channel = modules.get(guild.voice_channels, name='Foo', bitrate=64000)

        Nested attribute matching:

        .. code-block:: python3

            channel = modules.get(client.get_all_channels(), guild__name='Cool', name='general')

        Parameters
        -----------
        iterable
            An iterable to search through.
        \*\*attrs
            Keyword arguments that denote attributes to search with.
    """

    _all = all
    attrget = attrgetter

    if len(attrs) == 1:
        k, v = attrs.popitem()
        pred = attrget(k.replace("__", "."))
        elems = []
        for elem in iterable:
            if pred(elem) == v:
                elems.append(elem)
        if len(elems) == 1:
            return elems[0]
        elif len(elems) > 1:
            return elems
        return None

    converted = [
        (attrget(attr.replace("__", ".")), value) for attr, value in attrs.items()
    ]
    
    elems = []

    for elem in iterable:
        if _all(pred(elem) == value for pred, value in converted):
            elems.append(elem)
    
    if len(elems) == 1:
        return elems[0]
    elif len(elems) > 1:
        return elems
    return None


def create_embed(title: str, description: t.Optional[str] = None, colour: int = constants.EMBED_COLOUR) -> modules.MyEmbed:
    """
        Create new embed.

        :param title: Embed title.
        :param description: Embed description.
        :param colour: Embed colour.
        :type title: str
        :type description: str
        :type colour: int
        :returns: New embed.
        :rtype: modules.MyEmbed
    """
    embed = modules.MyEmbed(title=title, description=description, colour=colour)
    embed.set_author(name=constants.EMBED_AUTHOR_NAME, url=constants.EMBED_AUTHOR_URL, icon_url=constants.EMBED_AUTHOR_ICON_URL)
    embed.set_footer(text=constants.EMBED_FOOTER, icon_url=constants.EMBED_AUTHOR_ICON_URL)
    embed.set_thumbnail(url=constants.EMBED_AUTHOR_ICON_URL)
    return embed


def has_ayn_role(member: discord.Member, roles: t.Union[list,str,int]) -> bool:
    """
        Check if member has any role.

        :param member: Member to check..
        :param roles: Roles to check.
        :type member: discord.Member
        :type roles: list, str, int
        :rtype: bool
    """
    if isinstance(roles, str) or isinstance(roles, int):
        roles = [roles]
        

    getter = functools.partial(discord.utils.get, member.roles)
    return any(getter(id=role) is not None if isinstance(role, int) else getter(name=role) is not None for role in roles)


def strftime_translate(txt: str) -> str:
    """
        Translate strftime output to Turkish.

        :param txt: strftime output.
        :type txt: str
        :rtype: str
    """
    b = {"Jan": "Ocak", "Feb": "Şubat", "Mar": "Mart", "Apr": "Nisa", "May": "Mayıs", "Jun": "Haziran", "Jul": "Temmuz", "Aug": "Ağustos", "Sep": "Eylül", "Oct": "Ekim", "Nov": "Kasım", "Dec": "Aralık"}

    for i in b:
        if i in txt:
            txt = txt.replace(i, b[i])

    return txt
