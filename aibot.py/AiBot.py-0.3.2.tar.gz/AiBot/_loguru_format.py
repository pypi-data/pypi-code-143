# +------------+---------------------------------+----------------------------+
# | Key        | Description                     | Attributes                 |
# +============+=================================+============================+
# | elapsed    | The time elapsed since the      | See |timedelta|            |
# |            | start of the program            |                            |
# +------------+---------------------------------+----------------------------+
# | exception  | The formatted exception if any, | ``type``, ``value``,       |
# |            | ``None`` otherwise              | ``traceback``              |
# +------------+---------------------------------+----------------------------+
# | extra      | The dict of attributes          | None                       |
# |            | bound by the user (see |bind|)  |                            |
# +------------+---------------------------------+----------------------------+
# | file       | The file where the logging call | ``name`` (default),        |
# |            | was made                        | ``path``                   |
# +------------+---------------------------------+----------------------------+
# | function   | The function from which the     | None                       |
# |            | logging call was made           |                            |
# +------------+---------------------------------+----------------------------+
# | level      | The severity used to log the    | ``name`` (default),        |
# |            | message                         | ``no``, ``icon``           |
# +------------+---------------------------------+----------------------------+
# | line       | The line number in the source   | None                       |
# |            | code                            |                            |
# +------------+---------------------------------+----------------------------+
# | message    | The logged message (not yet     | None                       |
# |            | formatted)                      |                            |
# +------------+---------------------------------+----------------------------+
# | module     | The module where the logging    | None                       |
# |            | call was made                   |                            |
# +------------+---------------------------------+----------------------------+
# | name       | The ``__name__`` where the      | None                       |
# |            | logging call was made           |                            |
# +------------+---------------------------------+----------------------------+
# | process    | The process in which the        | ``name``, ``id`` (default) |
# |            | logging call was made           |                            |
# +------------+---------------------------------+----------------------------+
# | thread     | The thread in which the         | ``name``, ``id`` (default) |
# |            | logging call was made           |                            |
# +------------+---------------------------------+----------------------------+
# | time       | The aware local time when the   | See |datetime|             |
# |            | logging call was made           |                            |
# +------------+---------------------------------+----------------------------+
#
#
# +------------------------------------+--------------------------------------+
# | Color (abbr)                       | Styles (abbr)                        |
# +====================================+======================================+
# | Black (k)                          | Bold (b)                             |
# +------------------------------------+--------------------------------------+
# | Blue (e)                           | Dim (d)                              |
# +------------------------------------+--------------------------------------+
# | Cyan (c)                           | Normal (n)                           |
# +------------------------------------+--------------------------------------+
# | Green (g)                          | Italic (i)                           |
# +------------------------------------+--------------------------------------+
# | Magenta (m)                        | Underline (u)                        |
# +------------------------------------+--------------------------------------+
# | Red (r)                            | Strike (s)                           |
# +------------------------------------+--------------------------------------+
# | White (w)                          | Reverse (v)                          |
# +------------------------------------+--------------------------------------+
# | Yellow (y)                         | Blink (l)                            |
# +------------------------------------+--------------------------------------+
# |                                    | Hide (h)                             |
# +------------------------------------+--------------------------------------+
