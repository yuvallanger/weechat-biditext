# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 by Oscar Morante <oscar@morante.eu>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# This script uses fribidi library to display rtl text properly

import weechat
from pyfribidi import log2vis, LTR

SCRIPT_NAME    = "biditext"
SCRIPT_AUTHOR  = "Oscar Morante <oscar@morante.eu>"
SCRIPT_VERSION = "2"
SCRIPT_LICENSE = "GPL3"
SCRIPT_DESC    = "Use fribidi to handle RTL text"


def filter_log1_to_log9(tags_str):
    """
    Filters 'log1' to 'log9' out of a tags string.
    Result is later used to construct a displayed message's tags string.
    """

    log1_to_log9 = ('log' + str(i) for i in range(10))
    tag_list = tags_str.split(',')
    no_log_tags = ','.join(
        tag
        for tag in tag_list
        if tag not in log1_to_log9
    )
    return no_log_tags


def biditext_cb(data, modifier, modifier_data, line):
    """
    biditext_cb does two things:
        * Logs a line untransformed using the `no_log` tag.
        * Displays the line after it was transformed with fribidi using the
          `no_show_non_bidied` tag.
    returns an empty line because the messages were already handled
    inside the body of the function.
    """

    ltr_line = log2vis(line, LTR)

    plugin_name, buffer_name, tags = modifier_data.split(';')
    buffer_pointer = weechat.buffer_search(plugin_name, buffer_name)

    no_show_non_bidied_tags = tags + ',no_show_non_bidied'
    no_log_tags = filter_log1_to_log9(tags) + ',no_log'

    weechat.prnt_date_tags(buffer_pointer, 0, no_show_non_bidied_tags, line)
    weechat.prnt_date_tags(buffer_pointer, 0, no_log_tags, ltr_line)

    return ""


if __name__ == "__main__":
    script_registered = weechat.register(
        SCRIPT_NAME,
        SCRIPT_AUTHOR,
        SCRIPT_VERSION,
        SCRIPT_LICENSE,
        SCRIPT_DESC,
        "",
        "",
    )
    if script_registered:
        weechat.hook_modifier(
            'weechat_print',
            'biditext_cb',
            '',
        )

