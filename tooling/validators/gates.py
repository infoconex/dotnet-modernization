#!/usr/bin/env python3
"""Run explicitly configured validation commands, retaining per-gate evidence."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

SCHEMA_VERSION = 1
MAX_TIMEOUT = 3600


def git(root, *args):
    try:
        p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True,
                           timeout=10, check=False)
        return p.stdout.strip() if p.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def load_plan(path):
    plan = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(plan, dict) or plan.get('schema_version') != SCHEMA_VERSION:
        raise ValueError('plan must have schema_version: 1')
    gates = plan.get('gates')
    if not isinstance(gates, list) or not gates:
        raise ValueError('plan must contain at least one gate')
    seen = set()
    for gate in gates:
        if not isinstance(gate, dict):
            raise ValueError('each gate must be an object')
        ident = gate.get('id')
        if not isinstance(ident, str) or not ident or not all(c.isalnum() or c in '-_' for c in ident):
            raise ValueError('gate ids must be nonempty alphanumeric, dash or underscore')
        if ident in seen:
            raise ValueError(f'duplicate gate id: {ident}')
        seen.add(ident)
        cmd = gate.get('command')
        if not isinstance(cmd, list) or not cmd or not all(isinstance(x, str) and x for x in cmd):
            raise ValueError(f'{ident}: command must be a nonempty argv string array; shell is not supported')
        t = gate.get('timeout_seconds', 300)
        if not isinstance(t, int) or isinstance(t, bool) or not 1 <= t <= MAX_TIMEOUT:
            raise ValueError(f'{ident}: timeout_seconds must be an integer between 1 and {MAX_TIMEOUT}')
        expected = gate.get('expected_exit_codes', [0])
        if not isinstance(expected, list) or not expected or not all(type(x) is int and 0 <= x <= 255 for x in expected):
            raise ValueError(f'{ident}: expected_exit_codes must be a nonempty list of 0..255 integers')
        if len(expected) != len(set(expected)):
            raise ValueError(f'{ident}: duplicated expected exit code')
        kind = gate.get('kind', 'positive')
        if kind not in ('positive', 'negative'):
            raise ValueError(f'{ident}: kind must be positive or negative')
        if kind == 'negative' and 0 in expected:
            raise ValueError(f'{ident}: a negative control must reject exit code 0')
        if kind == 'positive' and expected != [0]:
            raise ValueError(f'{ident}: positive controls must require exit code 0')
        check = gate.get('nunit_xml')
        if check is not None:
            if kind != 'positive' or not isinstance(check, dict) or not isinstance(check.get('path'), str):
                raise ValueError(f'{ident}: nunit_xml must specify a path on a positive gate')
            if set(check) - {'path', 'expected'}:
                raise ValueError(f'{ident}: unsupported nunit_xml fields')
            want = check.get('expected')
            if not isinstance(want, dict) or not want or any(k not in {'total','passed','failed','skipped'} or type(v) is not int or v < 0 for k, v in want.items()):
                raise ValueError(f'{ident}: nunit_xml.expected requires nonnegative test counts')
    return plan


def within(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError('path must be a nonempty string')
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError('paths must remain inside application source directory')
    return target


def nunit_counts(path):
    tree = ET.parse(path).getroot()
    if tree.tag.rsplit('}', 1)[-1] != 'test-run':
        raise ValueError('expected NUnit 3 <test-run> XML root')
    return {k: int(tree.attrib[k]) for k in ('total', 'passed', 'failed', 'skipped')}


def run_plan(plan, source, evidence_dir, fail_fast=False):
    source = Path(source).resolve(strict=True)
    if not source.is_dir():
        raise ValueError('source must be an existing directory')
    evidence_dir = Path(evidence_dir).resolve()
    if evidence_dir == source or evidence_dir.is_relative_to(source):
        raise ValueError('evidence directory must be outside application checkout to avoid source contamination')
    evidence_dir.mkdir(parents=True, exist_ok=True)
    commit = git(source, 'rev-parse', 'HEAD')
    expected_commit = plan.get('expected_commit')
    if expected_commit and (not isinstance(expected_commit, str) or len(expected_commit) != 40):
        raise ValueError('expected_commit must be a full 40-character Git SHA')
    report = {'schema_version': SCHEMA_VERSION, 'kind': 'executed-validation-gates',
        'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'application': plan.get('application'), 'source': {'root': str(source), 'commit': commit,
        'expected_commit': expected_commit, 'dirty_before': (git(source, 'status', '--porcelain') or '').splitlines()},
        'host': {'os': platform.platform(), 'python': platform.python_version()},
        'gates': [], 'summary': {}, 'overall': 'not_executed'}
    if expected_commit and commit != expected_commit:
        raise ValueError('checkout commit differs from plan expected_commit; no validation gates executed')
    aborted = False
    for gate in plan['gates']:
        ident = gate['id']
        result = {'id': ident, 'kind': gate.get('kind', 'positive'), 'command': gate['command'],
                  'expected_exit_codes': gate.get('expected_exit_codes', [0]),
                  'status': 'not_executed', 'exit_code': None, 'duration_seconds': 0.0,
                  'log': f'{ident}.log'}
        report['gates'].append(result)
        if aborted:
            result['reason'] = 'fail-fast after an earlier gate failure'
            result['log'] = None
            continue
        log_file = evidence_dir / f'{ident}.log'
        try:
            cwd = within(source, gate.get('cwd', '.'))
            if not cwd.is_dir():
                raise ValueError('gate cwd does not exist')
            # The runner never uses a shell. Only trusted, reviewed plans should be executed.
            begin = time.monotonic()
            with log_file.open('wb') as log:
                try:
                    execution = subprocess.run(gate['command'], cwd=cwd, stdout=log,
                                               stderr=subprocess.STDOUT,
                                               timeout=gate.get('timeout_seconds', 300), check=False)
                    result['exit_code'] = execution.returncode
                    status = 'expected_negative' if gate.get('kind') == 'negative' else 'passed'
                    result['status'] = status if execution.returncode in result['expected_exit_codes'] else 'failed'
                except subprocess.TimeoutExpired:
                    result['status'] = 'timed_out'
                    result['reason'] = 'command exceeded timeout_seconds'
            result['duration_seconds'] = round(time.monotonic() - begin, 3)
            if result['status'] == 'passed' and gate.get('nunit_xml'):
                check = gate['nunit_xml']
                xml_path = within(source, check['path'])
                actual = nunit_counts(xml_path)
                result['nunit'] = {'observed': actual, 'expected': check['expected']}
                if any(actual.get(k) != v for k, v in check['expected'].items()):
                    result['status'] = 'failed'
                    result['reason'] = 'NUnit counts differ from expected baseline'
        except FileNotFoundError as ex:
            result['status'] = 'blocked'
            result['reason'] = f'command or evidence file absent: {str(ex)[:240]}'
        except (ValueError, ET.ParseError, KeyError) as ex:
            result['status'] = 'failed'
            result['reason'] = f'invalid result or gate path: {str(ex)[:240]}'
        except OSError as ex:
            result['status'] = 'blocked'
            result['reason'] = f'host I/O error: {str(ex)[:240]}'
        if fail_fast and result['status'] not in ('passed', 'expected_negative'):
            aborted = True
    statuses = ['passed', 'expected_negative', 'failed', 'blocked', 'timed_out', 'not_executed']
    report['summary'] = {status: sum(g['status'] == status for g in report['gates']) for status in statuses}
    report['overall'] = 'passed' if (report['summary']['passed'] + report['summary']['expected_negative'] == len(report['gates'])) else 'incomplete_or_failed'
    report['source']['dirty_after'] = (git(source, 'status', '--porcelain') or '').splitlines()
    (evidence_dir / 'results.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--plan', type=Path, required=True, help='Trusted JSON plan file')
    p.add_argument('--source', type=Path, required=True, help='Disposable application checkout')
    p.add_argument('--evidence-dir', type=Path, required=True, help='Output directory OUTSIDE checkout')
    p.add_argument('--fail-fast', action='store_true')
    args = p.parse_args(argv)
    try:
        plan = load_plan(args.plan)
        report = run_plan(plan, args.source, args.evidence_dir, args.fail_fast)
        print(f"Validation: {report['overall']} | {report['summary']} | {args.evidence_dir}/results.json")
        return 0 if report['overall'] == 'passed' else 1
    except (OSError, ValueError, json.JSONDecodeError) as ex:
        print(f'ERROR: {ex}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
