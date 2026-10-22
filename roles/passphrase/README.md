<!-- roles/passphrase/README.md
  -- ==========================
  --
  -- Copying
  -- -------
  --
  -- Copyright (c) 2026 universe.security authors and contributors.
  --
  -- This file is part of the *universe.security* project.
  --
  -- *universe.security* is a free software project. You can redistribute it
  -- and/or modify it following the terms of the MIT License.
  --
  -- This software project is distributed *as is*, WITHOUT WARRANTY OF ANY KIND;
  -- including but not limited to the WARRANTIES OF MERCHANTABILITY, FITNESS FOR
  -- A PARTICULAR PURPOSE and NONINFRINGEMENT.
  --
  -- You should have received a copy of the MIT License along with
  -- *universe.security*. If not, see <http://opensource.org/licenses/MIT>.
  -->

universe.security.passphrase
============================

Purpose
-------

The `universe.security.passphrase` role generates a passphrase using dice roll
sequences based on the [Electronic Frontier Foundation (EFF)](
https://www.eff.org/dice) wordlist.

Variables
---------

The role exposes the following variables for its configuration:

`passphrase_words_count` (Default: `6`)
: Number of words to include in the generated passphrase.

`passphrase_words_separator` (Default: `"-"`)
: String used as a separator between words in the generated passphrase.

Facts
-----

The role emits the following fact:

`passphrase_result`
: The generated passphrase string.
