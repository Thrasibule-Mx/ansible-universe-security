<!-- roles/passphrase/scripts/README.md
  -- ==================================
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

Scripts
=======

Purpose
-------

This directory contains utility and maintenance scripts for the
`universe.security.passphrase` role.

Listing
-------

`wordlist2json.py`
: Transform an Electronic Frontier Foundation (EFF) wordlist file into JSON.
Downloads the wordlist directly from the EFF website or reads from a local file,
and outputs either a flat key-value dictionary (default) or a nested dictionary
structure (using `-x`, `--extend`).
