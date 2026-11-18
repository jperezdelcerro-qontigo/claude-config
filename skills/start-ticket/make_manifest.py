#!/usr/bin/env python3
"""Create dbtools/manifests/<ticket>.xlsx from the Blank Template.

usage: make_manifest.py AN-12345 rows.json
rows.json: [[Database, Object Name, Object Type, Base Table or null, Schema], ...]
"""
import json
import os
import sys
import warnings

from openpyxl import load_workbook

TYPES = {'BCP_IN_FILE', 'DATA_SCRIPT', 'DDL_SCRIPT', 'DEFAULT_DATA_PROC', 'INDEX', 'STORED_PROC',
         'TABLE', 'TRIGGER', 'TRIGGER_ON_VIEW', 'VIEW', 'FUNCTION'}


def main(ticket, rowsPath):
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    manifests = os.path.join(root, 'dbtools', 'manifests')
    with open(rowsPath) as f:
        rows = json.load(f)
    for r in rows:
        if len(r) != 5 or r[2] not in TYPES:
            sys.exit('Bad row (need 5 columns and a valid Object Type): %r' % (r,))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        wb = load_workbook(os.path.join(manifests, 'Blank Template.xlsx'))
    sheet = wb['Template']
    for r in rows:
        sheet.append(r)
    out = os.path.join(manifests, ticket + '.xlsx')
    wb.save(out)
    print('Wrote %s (%d rows)' % (out, len(rows)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1].upper(), sys.argv[2])
