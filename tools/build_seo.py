#!/usr/bin/env python3
"""Run every HTML generator and the sitemap. --check is entirely non-writing."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def commands(check=False):
    tools=ROOT/'tools'
    builders=sorted(tools.glob('build_*_site.py'))
    builders += [tools/'build_gateways.py',tools/'build_jekyll_seo.py']
    result=[[sys.executable,str(p)] for p in builders]
    result.append(['node',str(tools/'build_nhip_chu_site.mjs')])
    result.append([sys.executable,str(tools/'build_sitemap.py')])
    return [cmd+(['--check'] if check else []) for cmd in result]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for command in commands(args.check):
        print('+ '+' '.join(command),flush=True)
        subprocess.run(command,cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(ROOT/'tools/check_seo.py')],cwd=ROOT,check=True)


if __name__=='__main__': main()
