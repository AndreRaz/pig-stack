#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 6 ]; then
  echo "usage: $0 <logfile> <phase> <decision> <why> <evidence> <result>" >&2
  exit 2
fi

logfile="$1"
mkdir -p "$(dirname "$logfile")"

if [ ! -s "$logfile" ]; then
  printf 'ts\tphase\tdecision\twhy\tevidence\tresult\n' > "$logfile"
fi

sanitize() {
  local v="$1"
  v="${v//$'\t'/ }"
  v="${v//$'\n'/ }"
  v="${v//$'\r'/ }"
  case "$v" in
    =*|+*) v="'$v" ;;
    -*|@*) v="'$v" ;;
  esac
  printf '%s' "$v"
}

ts="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
phase="$(sanitize "$2")"
decision="$(sanitize "$3")"
why="$(sanitize "$4")"
evidence="$(sanitize "$5")"
result="$(sanitize "$6")"

printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$ts" "$phase" "$decision" "$why" "$evidence" "$result" >> "$logfile"
