"""Original synthetic report boundary cases; no external approval claims."""
import copy
import hashlib
import importlib
import json
import os
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
DIGEST = "sha256:" + "a" * 64


def report():
    return {"report_id": "synthetic-report", "artifact_ref": "artifact.txt",
            "artifact_digest": DIGEST, "ruleset_version": "0.1.0",
            "profile": "web-editorial", "checks": [{"rule_id": "CONTENT-001",
            "status": "passed", "method": "manual", "evidence_refs": ["observed.txt"],
            "scope": "whole", "reason": "Original synthetic observation."}],
            "environment": {"host": "synthetic", "tools": {}, "renderers": []},
            "limitations": ["Structural fixture only."], "content_change_summary": []}


def rule():
    return {"id": "CONTENT-001", "revision": 1, "title_ja": "合成確認",
            "requirement_en": "Compare supplied original text.", "kind": "project-policy",
            "strength": "must", "impact": "error", "media": ["web-editorial"],
            "source_refs": ["policy:synthetic"], "conditions": [],
            "verification": {"method": "manual", "coverage": "planned"},
            "fix_policy": {"mode": "review-only", "protected_content": [], "guidance": "Observe."},
            "exception_policy": {"allowed": True, "bounds": "One exact scope.", "approval_required": True},
            "case_ids": []}


class SyntheticHost:
    """Explicit inherited test capability; not real approval/authentication."""
    def __init__(self, directory):
        self.directory=Path(directory); self.directory.mkdir(mode=0o700)
        now=datetime.now(timezone.utc)
        stamp=lambda dt: dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.issued=stamp(now-timedelta(minutes=10)); self.expires=stamp(now+timedelta(hours=1))
        self.data={'format':'kumihan-host-authority-1','generation':1,'principals':{'synthetic-principal':{'identity_ref':'synthetic-identity-proof','state':'active'}},
                   'grants':[], 'observations':[], 'approvals':[], 'approval_states':[], 'procedures':[], 'chronologies':[]}
        self.path=self.directory/'authority.json'; self.fd=None

    def save(self):
        if not self.path.exists():
            fd=os.open(self.path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600); os.close(fd)
        self.path.write_text(json.dumps(self.data))

    def __enter__(self):
        self.save(); self.fd=os.open(self.directory,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        self.environment=patch.dict(os.environ,{'KUMIHAN_HOST_CONTEXT_FD':str(self.fd)})
        self.environment.__enter__(); return self

    def __exit__(self,*args):
        self.environment.__exit__(*args); os.close(self.fd)

    def grant(self, purpose, item, scope, bounds):
        self.data['grants'].append({'principal_ref':'synthetic-principal','purpose':purpose,'rule_id':item['id'],'scope':scope,
            'bounds':bounds,'issued_at':self.issued,'expires_at':self.expires,'state':'current'})

    def observe(self, value, item, evidence):
        check=value['checks'][0]
        self.grant('observation',item,check['scope'],value['artifact_digest'])
        self.data['observations'].append({'reference':check['evidence_refs'][0],'report_id':value['report_id'],
            'rule_id':item['id'],'scope':check['scope'],'artifact_ref':value['artifact_ref'],'artifact_digest':value['artifact_digest'],
            'method':check['method'],'evidence_digest':'sha256:'+hashlib.sha256(evidence).hexdigest(),'observed_at':self.issued,
            'observer_ref':'synthetic-principal','status':'passed'})

    def approve(self, value, item):
        check=value['checks'][0]; waiver=check['waiver']
        self.grant('report-waiver',item,check['scope'],item['exception_policy']['bounds'])
        self.data['approvals'].append({'approval_ref':waiver['approval_ref'],'purpose':'report-waiver','approver_ref':'synthetic-principal',
            'issued_at':self.issued,'expires_at':self.expires,'scope':waiver['scope'],'reason':waiver['reason'],
            'subject':{k:value[k] for k in ('report_id','artifact_ref','artifact_digest')}|{'rule_id':item['id']},'state':'current','revision':1})
        self.data['approval_states'].append({'approval_ref':waiver['approval_ref'],'revision':1,'state':'current'})

    def procedure(self, item):
        from scripts.validate_catalog import binding_digest
        digest=binding_digest(item)
        self.grant('procedure-admission',item,'catalog',digest)
        def file(name,data):
            path=self.directory/name; fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as handle: handle.write(data)
            return {'path':name,'digest':'sha256:'+hashlib.sha256(data).hexdigest()}
        definition=file('procedure.md',b'Original synthetic documented review procedure.\n')
        tests=file('procedure-tests.json',json.dumps({'case_ids':item['case_ids'],'original':'synthetic'}).encode())
        result=file('procedure-result.json',json.dumps({'rule_id':item['id'],'rule_digest':digest,'method':item['verification']['method'],
            'definition_digest':definition['digest'],'test_digests':[tests['digest']], 'case_ids':item['case_ids'],'status':'passed','tested_at':self.issued}).encode())
        self.data['procedures'].append({'rule_id':item['id'],'rule_digest':digest,'method':item['verification']['method'],
            'kind':'detector' if item['verification']['method']=='static' else 'review-procedure','reviewer_ref':'synthetic-principal',
            'definition':definition,'tests':[tests],'result':result,'state':'current'})


class ReportTests(unittest.TestCase):
    def setUp(self):
        try:
            self.validate = importlib.import_module("scripts.validate_report").validate_report
        except ImportError:
            self.fail("Frozen validate_report callable is not implemented")

    def test_valid_structural_report_does_not_authenticate_evidence(self):
        value = report()
        original = copy.deepcopy(value)
        self.assertEqual(self.validate(value, [rule()]), [])
        self.assertEqual(value, original)

    def test_reject_invalid_shapes_without_coercion(self):
        changes = [("artifact_digest", None), ("extra", "unsafe"), ("ruleset_version", "0.1.0+meta")]
        for key, value in changes:
            with self.subTest(key=key):
                item = report(); item[key] = value
                self.assertTrue(self.validate(item, [rule()]))
        for status in [True, "PASS", "passed ", 1, None]:
            with self.subTest(status=status):
                item = report(); item["checks"][0]["status"] = status
                self.assertTrue(self.validate(item, [rule()]))
                self.assertIs(item["checks"][0]["status"], status)
        for item in [None, [], {}, {"checks": None}]:
            self.assertTrue(self.validate(item, [rule()]))

    def test_all_statuses_remain_distinct(self):
        for status in ["passed", "failed", "needs-review", "not-checked", "unsupported", "not-applicable", "waived"]:
            item = report(); item["checks"][0]["status"] = status
            if status == "waived":
                item["checks"][0]["waiver"] = {"approval_ref": "opaque", "scope": "whole",
                                              "reason": "Bounded synthetic exception.", "artifact_digest": DIGEST}
            self.assertEqual(self.validate(item, [rule()]), [])
            self.assertEqual(item["checks"][0]["status"], status)

    def test_pass_needs_nonblank_evidence_and_method(self):
        for evidence in [[], [" "], None]:
            item = report(); item["checks"][0]["evidence_refs"] = evidence
            self.assertTrue(self.validate(item, [rule()]))
        item = report(); del item["checks"][0]["method"]
        self.assertTrue(self.validate(item, [rule()]))

    def test_diagnostics_do_not_echo_untrusted_keys(self):
        item = report(); item["environment"]["tools"] = {"UNTRUSTED-CONTROL\n": 42}
        self.assertNotIn("UNTRUSTED-CONTROL", " ".join(self.validate(item, [rule()])))

    def test_unimplemented_static_pass_is_rejected(self):
        item = report(); item["checks"][0]["method"] = "static"
        catalog_rule = rule(); catalog_rule["verification"]["method"] = "static"
        self.assertTrue(self.validate(item, [catalog_rule]))

    def test_duplicate_keys_and_catalog_relationships(self):
        item = report(); item["checks"].append(copy.deepcopy(item["checks"][0]))
        self.assertTrue(self.validate(item, [rule()]))
        item["checks"][1]["scope"] = "section-2"
        self.assertEqual(self.validate(item, [rule()]), [])
        self.assertTrue(self.validate(report(), []))
        self.assertTrue(self.validate(report(), [rule(), rule()]))
        item = report(); item["checks"][0]["method"] = "static"
        self.assertTrue(self.validate(item, [rule()]))

    def test_wrong_artifact_scope_and_disallowed_waiver(self):
        item = report(); check = item["checks"][0]; check["status"] = "waived"
        check["waiver"] = {"approval_ref": "opaque", "scope": "whole", "reason": "Synthetic exception.", "artifact_digest": DIGEST}
        for key, value in [("scope", "elsewhere"), ("artifact_digest", "sha256:" + "b" * 64)]:
            bad = copy.deepcopy(item); bad["checks"][0]["waiver"][key] = value
            self.assertTrue(self.validate(bad, [rule()]))
        disallowed = rule(); disallowed["exception_policy"]["allowed"] = False
        self.assertTrue(self.validate(item, [disallowed]))
        check["status"] = "passed"
        self.assertTrue(self.validate(item, [rule()]))

    def test_local_evidence_missing_wrong_artifact_and_untrusted_waiver_fail_closed(self):
        from scripts.validate_report import admission_errors
        local_evidence_errors=lambda root,value: admission_errors(root,value,[rule()])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); value = report()
            self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))
            (root / "artifact.txt").write_bytes(b"Original synthetic target.\n")
            (root / "observed.txt").write_bytes(b"Original synthetic observation.\n")
            self.assertIn("report: local artifact digest mismatch", local_evidence_errors(root, value))
            value["artifact_digest"] = "sha256:" + hashlib.sha256((root / "artifact.txt").read_bytes()).hexdigest()
            self.assertIn("report: trusted host identity/authority/current-state/binding evidence unavailable or invalid", local_evidence_errors(root, value))
            value["checks"][0]["status"] = "waived"
            self.assertIn("report: trusted host identity/authority/current-state/binding evidence unavailable or invalid", local_evidence_errors(root, value))
            for path in ["../outside", "/etc/passwd", "C:\\escape", "\\\\host\\share"]:
                value["checks"][0]["evidence_refs"] = [path]
                self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))
            (root / "alias").symlink_to(root / "observed.txt")
            value["checks"][0]["evidence_refs"] = ["alias"]
            self.assertIn("report: missing or unsafe local artifact/evidence", local_evidence_errors(root, value))

    def test_cli_complete_fixture_context_keeps_admission_limits_and_exits(self):
        from test_catalog import complete_root
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); complete_root(root)
            artifact = b"Original synthetic target.\n"
            (root / "artifact.txt").write_bytes(artifact)
            (root / "observed.txt").write_text("Original synthetic observation.\n")
            value = report(); value["artifact_digest"] = "sha256:" + hashlib.sha256(artifact).hexdigest()
            path = root / "report.json"
            for status, expected in [("not-checked", 0), ("failed", 1), ("passed", 2), ("waived", 2)]:
                value["checks"][0]["status"] = status
                if status == "waived":
                    value["checks"][0]["waiver"] = {"approval_ref": "synthetic-unverified", "scope": "whole", "reason": "Synthetic request.", "artifact_digest": value["artifact_digest"]}
                path.write_text(json.dumps(value))
                result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_report.py"), "--root", str(root), "--report", str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stdout)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(json.loads(path.read_text())["checks"][0]["status"], status)


class CycleOneReportRegressions(unittest.TestCase):
    def test_host_proof_reads_stay_inside_inherited_directory(self):
        from scripts.validate_catalog import HostAuthority
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); host=SyntheticHost(base/'host')
            trusted=b'Original synthetic retained proof.'
            (host.directory/'proof.txt').write_bytes(trusted)
            reference={'path':'proof.txt','digest':'sha256:'+hashlib.sha256(trusted).hexdigest()}
            with host:
                authority=HostAuthority(base/'data')
                host.directory.rename(base/'retained')
                host.directory.mkdir(mode=0o700)
                (host.directory/'proof.txt').write_bytes(b'Untrusted replacement proof.')
                self.assertEqual(authority.record_file(reference),trusted)

    def test_r01_positive_host_observation_and_host_waiver_cli(self):
        from test_catalog import complete_root
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); root=base/'data'; root.mkdir(); rules=complete_root(root)
            artifact=b'Original synthetic artifact.\n'; evidence=b'Original synthetic observed record.\n'
            (root/'artifact.txt').write_bytes(artifact); (root/'observed.txt').write_bytes(evidence)
            value=report(); value['artifact_digest']='sha256:'+hashlib.sha256(artifact).hexdigest()
            path=root/'report.json'
            for status in ('passed','waived'):
                value['checks'][0]['status']=status
                if status=='waived': value['checks'][0]['waiver']={'approval_ref':'synthetic-approval','scope':'whole','reason':'Synthetic bounded waiver.','artifact_digest':value['artifact_digest']}
                host=SyntheticHost(base/('host-'+status)); host.observe(value,rules[0],evidence)
                if status=='waived': host.approve(value,rules[0])
                path.write_text(json.dumps(value))
                with host:
                    result=subprocess.run([sys.executable,str(ROOT/'scripts/validate_report.py'),'--root',str(root),'--report',str(path)],
                        capture_output=True,text=True,pass_fds=(host.fd,))
                    with self.subTest(status=status): self.assertEqual(result.returncode,0,result.stdout)
                    self.assertEqual(json.loads(path.read_text())['checks'][0]['status'],status)

    def test_r01_reject_self_authority_and_hostile_approval_states(self):
        from scripts.validate_report import admission_errors
        local_evidence_errors=lambda root,value: admission_errors(root,value,[rule()])
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); root=base/'data'; root.mkdir(); item=rule(); value=report()
            artifact=b'synthetic'; (root/'artifact.txt').write_bytes(artifact); (root/'observed.txt').write_bytes(b'observed')
            value['artifact_digest']='sha256:'+hashlib.sha256(artifact).hexdigest(); value['checks'][0]['status']='waived'
            value['checks'][0]['waiver']={'approval_ref':'synthetic-approval','scope':'whole','reason':'Synthetic request.','artifact_digest':value['artifact_digest']}
            host=SyntheticHost(base/'host'); host.approve(value,item)
            with host:
                from scripts.validate_report import admission_errors
                self.assertEqual(admission_errors(root,value,[item]),[])
                original=json.loads(json.dumps(host.data))
                for kind in ('revoked','superseded','boolean-revision','wrong-scope','wrong-subject','wrong-reason','missing-approver','missing-expiry','expired','not-issued','offset','invalid-calendar','leap-second','fractional','unauthorized','ambiguous'):
                    host.data=json.loads(json.dumps(original)); approval=host.data['approvals'][0]
                    if kind in ('revoked','superseded'): host.data['approval_states'][0]['state']=kind
                    elif kind=='boolean-revision': host.data['approval_states'][0]['revision']=True
                    elif kind=='wrong-scope': approval['scope']='other'
                    elif kind=='wrong-subject': approval['subject']['artifact_digest']='sha256:'+'b'*64
                    elif kind=='wrong-reason': approval['reason']='other'
                    elif kind=='missing-approver': del approval['approver_ref']
                    elif kind=='missing-expiry': del approval['expires_at']
                    elif kind=='expired': approval['expires_at']='2000-01-01T00:00:00Z'
                    elif kind=='not-issued': approval['issued_at']='2099-01-01T00:00:00Z'
                    elif kind=='offset': approval['issued_at']='2026-01-01T00:00:00+00:00'
                    elif kind=='invalid-calendar': approval['issued_at']='2026-02-30T00:00:00Z'
                    elif kind=='leap-second': approval['issued_at']='2026-01-01T00:00:60Z'
                    elif kind=='fractional': approval['issued_at']='2026-01-01T00:00:00.0Z'
                    elif kind=='unauthorized': host.data['grants']=[]
                    elif kind=='ambiguous': host.data['approvals'].append(approval)
                    host.save()
                    with self.subTest(kind=kind): self.assertTrue(admission_errors(root,value,[item]))
            hostile=SyntheticHost(root/'self-authority'); hostile.data=original
            with hostile: self.assertTrue(admission_errors(root,value,[item]))


    def test_r01_half_open_expiry_and_atomic_latest_state(self):
        from scripts.validate_catalog import utc_stamp
        from scripts.validate_report import admission_errors
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); root=base/'data'; root.mkdir(); item=rule(); value=report()
            data=b'original synthetic'; (root/'artifact.txt').write_bytes(data); (root/'observed.txt').write_bytes(b'observed')
            value['artifact_digest']='sha256:'+hashlib.sha256(data).hexdigest(); value['checks'][0]['status']='waived'
            value['checks'][0]['waiver']={'approval_ref':'synthetic-approval','scope':'whole','reason':'Synthetic request.','artifact_digest':value['artifact_digest']}
            host=SyntheticHost(base/'host'); host.approve(value,item)
            with host:
                expires=utc_stamp(host.expires)
                with patch('scripts.validate_catalog.utc_now',return_value=expires-timedelta(microseconds=1)):
                    self.assertEqual(admission_errors(root,value,[item]),[])
                with patch('scripts.validate_catalog.utc_now',return_value=expires):
                    self.assertTrue(admission_errors(root,value,[item]))
                host.data['approval_states'][0]['state']='revoked'
                replacement=host.directory/'replacement.json'; fd=os.open(replacement,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
                with os.fdopen(fd,'w') as handle: json.dump(host.data,handle)
                replacement.replace(host.path)
                self.assertTrue(admission_errors(root,value,[item]))


    def test_r01_design_chronology_and_no_retroactive_waiver(self):
        from scripts.validate_report import admission_errors
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); root=base/'data'; root.mkdir(); item=rule(); value=report()
            artifact=b'original synthetic output'; (root/'artifact.txt').write_bytes(artifact)
            value['artifact_digest']='sha256:'+hashlib.sha256(artifact).hexdigest()
            contract={'brief_id':'synthetic-brief','medium':'web-editorial','audience':'Synthetic readers','objective':'Compare original choices.',
                'primary_information':['Original synthetic choice.'],'primary_action':'Read the choice.', 'structure_rationale':'Original sequence supports the stated comparison.',
                'type_roles':[{'role':'body','family':'host-available','size':'1rem','rationale':'Original synthetic role.'}],
                'asset_provenance':[],'brand_constraints':[],'rejected_defaults':[],'exceptions':[],'created_before_generation':True}
            encoded=json.dumps(contract).encode(); (root/'design.json').write_bytes(encoded)
            value['checks'][0]['evidence_refs']=['design.json']
            host=SyntheticHost(base/'host'); host.observe(value,item,encoded)
            now=datetime.now(timezone.utc); stamp=lambda dt:dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            host.data['observations'][0]['observed_at']=stamp(now-timedelta(minutes=1))
            digest='sha256:'+hashlib.sha256(encoded).hexdigest(); host.grant('generate',item,'whole',digest)
            brief=json.dumps({'brief_id':'synthetic-brief','source':'Original retained synthetic brief.'}).encode()
            fd=os.open(host.directory/'brief.json',os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as handle: handle.write(brief)
            chronology={'brief_id':'synthetic-brief','design_contract_digest':digest,'artifact_digest':value['artifact_digest'],
                'created_at':stamp(now-timedelta(minutes=8)),'generation_started_at':stamp(now-timedelta(minutes=5)),
                'owner_ref':'synthetic-principal','scope':'whole','mode':'generate',
                'brief':{'path':'brief.json','digest':'sha256:'+hashlib.sha256(brief).hexdigest()}}
            host.data['chronologies']=[chronology]
            with host:
                self.assertEqual(admission_errors(root,value,[item]),[])
                request={'approval_ref':'synthetic-design-exception','scope':'whole','reason':'Original synthetic bounded exception.'}
                contract['exceptions']=[request]; encoded=json.dumps(contract).encode(); (root/'design.json').write_bytes(encoded)
                digest='sha256:'+hashlib.sha256(encoded).hexdigest()
                chronology['design_contract_digest']=digest
                host.data['observations'][0]['evidence_digest']=digest
                host.data['grants'][1]['bounds']=digest
                host.grant('design-exception',item,'whole',item['exception_policy']['bounds'])
                host.data['approvals'].append(request|{'purpose':'design-exception','approver_ref':'synthetic-principal',
                    'issued_at':host.issued,'expires_at':host.expires,'state':'current','revision':1,
                    'subject':{'brief_id':contract['brief_id'],'design_contract_digest':digest}})
                host.data['approval_states'].append({'approval_ref':request['approval_ref'],'revision':1,'state':'current'})
                host.save(); self.assertEqual(admission_errors(root,value,[item]),[])
                host.data['approval_states'][0]['state']='revoked'; host.save()
                self.assertTrue(admission_errors(root,value,[item]))
                host.data['approval_states'][0]['state']='current'
                chronology['created_at']=stamp(now-timedelta(minutes=2)); host.save()
                self.assertTrue(admission_errors(root,value,[item]))
                value['checks'][0]['status']='waived'; value['checks'][0]['waiver']={'approval_ref':'synthetic-waiver','scope':'whole','reason':'Synthetic request.','artifact_digest':value['artifact_digest']}
                host.approve(value,item); host.save()
                self.assertTrue(admission_errors(root,value,[item]))


class CycleTwoReportRegressions(unittest.TestCase):
    def test_r01_final_artifact_and_evidence_binding(self):
        from scripts.validate_catalog import HostAuthority
        from scripts.validate_report import admission_errors
        for target in ('artifact.txt','observed.txt'):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                base=Path(directory); root=base/'data'; root.mkdir(); value=report(); item=rule()
                artifact=b'Original stable synthetic artifact.'; evidence=b'Original stable observation.'
                (root/'artifact.txt').write_bytes(artifact); (root/'observed.txt').write_bytes(evidence)
                value['artifact_digest']='sha256:'+hashlib.sha256(artifact).hexdigest()
                host=SyntheticHost(base/'host'); host.observe(value,item,evidence)
                lookup=HostAuthority.lookup
                def change(authority,group,predicate):
                    result=lookup(authority,group,predicate)
                    if group=='observations': (root/target).write_bytes(b'Changed during admission.')
                    return result
                with host, patch.object(HostAuthority,'lookup',change):
                    self.assertTrue(admission_errors(root,value,[item]))

    def test_r01_design_role_cannot_be_selected_by_suffix(self):
        from scripts.validate_report import admission_errors
        from test_catalog import complete_root
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory); root=base/'data'; root.mkdir(); rules=complete_root(root)
            item=next(r for r in rules if r['id']=='DESIGN-001'); value=report(); value['checks'][0]['rule_id']=item['id']
            artifact=b'Original synthetic design output.'; (root/'artifact.txt').write_bytes(artifact)
            value['artifact_digest']='sha256:'+hashlib.sha256(artifact).hexdigest()
            contract={'brief_id':'synthetic-brief','medium':'web-editorial','audience':'Synthetic audience','objective':'Original intent.',
                'primary_information':['Original information.'],'primary_action':'Read.','structure_rationale':'Original order.',
                'type_roles':[{'role':'body','family':'host-available','size':'1rem','rationale':'Original role.'}],
                'asset_provenance':[],'brand_constraints':[],'rejected_defaults':[],'exceptions':[],'created_before_generation':True}
            data=json.dumps(contract).encode(); now=datetime.now(timezone.utc); stamp=lambda dt:dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            for filename in ('design.json','design.txt','design.data'):
                value['checks'][0]['evidence_refs']=[filename]; (root/filename).write_bytes(data)
                host=SyntheticHost(base/('host-'+filename)); host.observe(value,item,data)
                host.data['observations'][0]['observed_at']=stamp(now-timedelta(minutes=1))
                digest='sha256:'+hashlib.sha256(data).hexdigest(); host.grant('generate',item,'whole',digest)
                brief=json.dumps({'brief_id':'synthetic-brief'}).encode(); (host.directory/'brief.json').write_bytes(brief)
                chronology={'brief_id':'synthetic-brief','design_contract_digest':digest,'artifact_digest':value['artifact_digest'],
                    'created_at':stamp(now-timedelta(minutes=2)),'generation_started_at':stamp(now-timedelta(minutes=5)),
                    'owner_ref':'synthetic-principal','scope':'whole','mode':'generate','brief':{'path':'brief.json','digest':'sha256:'+hashlib.sha256(brief).hexdigest()}}
                host.data['chronologies']=[chronology]
                with host:
                    with self.subTest(filename=filename): self.assertTrue(admission_errors(root,value,rules))
                    path=root/'report.json'; path.write_text(json.dumps(value))
                    result=subprocess.run([sys.executable,str(ROOT/'scripts/validate_report.py'),'--root',str(root),'--report',str(path)],capture_output=True,text=True,pass_fds=(host.fd,))
                    with self.subTest(cli=filename): self.assertEqual(result.returncode,2,result.stdout)
                    chronology['created_at']=stamp(now-timedelta(minutes=8)); host.save()
                    self.assertEqual(admission_errors(root,value,rules),[])
                    chronology['created_at']=stamp(now-timedelta(minutes=2))


if __name__ == "__main__":
    unittest.main()
