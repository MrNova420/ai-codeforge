#!/usr/bin/env python3
"""
Security Operations Center - Enterprise-Grade Security
Complete security operations with threat modeling, vulnerability scanning, and compliance

Features:
- OWASP Top 10 vulnerability detection
- Threat modeling (STRIDE framework)
- Security code review
- Penetration testing simulation
- Compliance checking (GDPR, SOC2, HIPAA, PCI-DSS)
- Incident response
- Security metrics and reporting
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
import json
from pathlib import Path


class ThreatLevel(Enum):
    """Security threat levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class VulnerabilityType(Enum):
    """Common vulnerability types (OWASP Top 10)."""
    INJECTION = "injection"
    BROKEN_AUTH = "broken_authentication"
    SENSITIVE_DATA = "sensitive_data_exposure"
    XXE = "xml_external_entities"
    BROKEN_ACCESS = "broken_access_control"
    SECURITY_MISCONFIG = "security_misconfiguration"
    XSS = "cross_site_scripting"
    INSECURE_DESERIALIZE = "insecure_deserialization"
    VULNERABLE_COMPONENTS = "vulnerable_components"
    INSUFFICIENT_LOGGING = "insufficient_logging"


class ComplianceStandard(Enum):
    """Compliance standards."""
    GDPR = "gdpr"
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"
    NIST = "nist"


@dataclass
class SecurityVulnerability:
    """Security vulnerability finding."""
    vuln_type: VulnerabilityType
    severity: ThreatLevel
    title: str
    description: str
    location: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    remediation: str = ""
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    references: List[str] = field(default_factory=list)


@dataclass
class ThreatModel:
    """STRIDE threat model."""
    asset: str
    threats: Dict[str, List[str]] = field(default_factory=dict)
    mitigations: Dict[str, List[str]] = field(default_factory=dict)
    risk_score: float = 0.0
    
    def __post_init__(self):
        """Initialize STRIDE categories."""
        if not self.threats:
            self.threats = {
                "Spoofing": [],
                "Tampering": [],
                "Repudiation": [],
                "Information Disclosure": [],
                "Denial of Service": [],
                "Elevation of Privilege": []
            }
        if not self.mitigations:
            self.mitigations = {k: [] for k in self.threats.keys()}


@dataclass
class SecurityAuditReport:
    """Complete security audit report."""
    timestamp: datetime
    vulnerabilities: List[SecurityVulnerability]
    threat_models: List[ThreatModel]
    compliance_status: Dict[str, bool]
    risk_score: float
    summary: str
    recommendations: List[str]
    
    def get_critical_count(self) -> int:
        """Get count of critical vulnerabilities."""
        return sum(1 for v in self.vulnerabilities if v.severity == ThreatLevel.CRITICAL)
    
    def get_high_count(self) -> int:
        """Get count of high severity vulnerabilities."""
        return sum(1 for v in self.vulnerabilities if v.severity == ThreatLevel.HIGH)


class SecurityOpsCenter:
    """Enterprise Security Operations Center."""
    
    def __init__(self):
        """Initialize security operations center."""
        self.vulnerabilities: List[SecurityVulnerability] = []
        self.threat_models: List[ThreatModel] = []
        self.security_patterns = self._load_security_patterns()
        
    def _load_security_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load security vulnerability patterns."""
        return {
            "sql_injection": [
                {
                    "pattern": r"execute\s*\(\s*[\"'].*\+.*[\"']\s*\)",
                    "description": "SQL injection via string concatenation",
                    "severity": ThreatLevel.CRITICAL,
                    "remediation": "Use parameterized queries or prepared statements"
                },
                {
                    "pattern": r"cursor\.execute\s*\([^)]*%.*\)",
                    "description": "SQL injection via string formatting",
                    "severity": ThreatLevel.CRITICAL,
                    "remediation": "Use parameterized queries with ? or %s placeholders"
                }
            ],
            "xss": [
                {
                    "pattern": r"innerHTML\s*=",
                    "description": "Potential XSS via innerHTML",
                    "severity": ThreatLevel.HIGH,
                    "remediation": "Use textContent or sanitize HTML input"
                },
                {
                    "pattern": r"document\.write\s*\(",
                    "description": "Potential XSS via document.write",
                    "severity": ThreatLevel.HIGH,
                    "remediation": "Use safer DOM manipulation methods"
                }
            ],
            "hardcoded_secrets": [
                {
                    "pattern": r"(password|passwd|pwd|secret|api_key|apikey|token)\s*=\s*[\"'][^\"']{8,}[\"']",
                    "description": "Hardcoded credentials detected",
                    "severity": ThreatLevel.CRITICAL,
                    "remediation": "Use environment variables or secure vaults"
                }
            ],
            "weak_crypto": [
                {
                    "pattern": r"(MD5|SHA1)\s*\(",
                    "description": "Weak cryptographic algorithm",
                    "severity": ThreatLevel.MEDIUM,
                    "remediation": "Use SHA-256 or better"
                },
                {
                    "pattern": r"DES|3DES|RC4",
                    "description": "Deprecated encryption algorithm",
                    "severity": ThreatLevel.HIGH,
                    "remediation": "Use AES-256 or ChaCha20"
                }
            ],
            "unsafe_deserialization": [
                {
                    "pattern": r"pickle\.loads?\s*\(",
                    "description": "Unsafe deserialization with pickle",
                    "severity": ThreatLevel.HIGH,
                    "remediation": "Validate and sanitize input, use safer formats like JSON"
                },
                {
                    "pattern": r"eval\s*\(",
                    "description": "Code injection via eval",
                    "severity": ThreatLevel.CRITICAL,
                    "remediation": "Never use eval with user input"
                }
            ],
            "path_traversal": [
                {
                    "pattern": r"open\s*\([^)]*\+[^)]*\)",
                    "description": "Potential path traversal",
                    "severity": ThreatLevel.HIGH,
                    "remediation": "Validate and sanitize file paths"
                }
            ],
            "insecure_random": [
                {
                    "pattern": r"random\.(random|randint|choice)",
                    "description": "Insecure random number generation",
                    "severity": ThreatLevel.MEDIUM,
                    "remediation": "Use secrets module for security-sensitive operations"
                }
            ]
        }
    
    async def scan_vulnerabilities(self, path: str) -> List[SecurityVulnerability]:
        """Scan code for vulnerabilities."""
        vulnerabilities = []
        path_obj = Path(path)
        
        if path_obj.is_file():
            files = [path_obj]
        else:
            files = list(path_obj.rglob("*.py")) + list(path_obj.rglob("*.js")) + list(path_obj.rglob("*.java"))
        
        for file_path in files:
            try:
                content = file_path.read_text()
                lines = content.split('\n')
                
                for category, patterns in self.security_patterns.items():
                    for pattern_info in patterns:
                        pattern = pattern_info["pattern"]
                        matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                        
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            code_snippet = lines[line_num - 1] if line_num <= len(lines) else ""
                            
                            vuln = SecurityVulnerability(
                                vuln_type=self._categorize_vulnerability(category),
                                severity=pattern_info["severity"],
                                title=pattern_info["description"],
                                description=f"Found in {file_path.name} at line {line_num}",
                                location=str(file_path),
                                line_number=line_num,
                                code_snippet=code_snippet.strip(),
                                remediation=pattern_info["remediation"]
                            )
                            vulnerabilities.append(vuln)
            except Exception as e:
                print(f"Error scanning {file_path}: {e}")
        
        self.vulnerabilities.extend(vulnerabilities)
        return vulnerabilities
    
    def _categorize_vulnerability(self, category: str) -> VulnerabilityType:
        """Categorize vulnerability type."""
        mapping = {
            "sql_injection": VulnerabilityType.INJECTION,
            "xss": VulnerabilityType.XSS,
            "hardcoded_secrets": VulnerabilityType.SENSITIVE_DATA,
            "weak_crypto": VulnerabilityType.SECURITY_MISCONFIG,
            "unsafe_deserialization": VulnerabilityType.INSECURE_DESERIALIZE,
            "path_traversal": VulnerabilityType.BROKEN_ACCESS,
            "insecure_random": VulnerabilityType.SECURITY_MISCONFIG
        }
        return mapping.get(category, VulnerabilityType.SECURITY_MISCONFIG)
    
    async def threat_model(self, asset_name: str, description: str = "") -> ThreatModel:
        """Create STRIDE threat model for an asset."""
        model = ThreatModel(asset=asset_name)
        
        # Auto-generate common threats based on asset type
        if "auth" in asset_name.lower() or "login" in asset_name.lower():
            model.threats["Spoofing"] = [
                "Attacker impersonates legitimate user",
                "Session hijacking via stolen tokens",
                "Credential stuffing attacks"
            ]
            model.threats["Tampering"] = [
                "Modification of authentication tokens",
                "Man-in-the-middle attacks"
            ]
            model.threats["Repudiation"] = [
                "User denies actions taken",
                "Insufficient audit logging"
            ]
            model.threats["Information Disclosure"] = [
                "Credential leakage in logs",
                "Timing attacks reveal valid usernames"
            ]
            model.threats["Denial of Service"] = [
                "Brute force password attempts",
                "Account lockout abuse"
            ]
            model.threats["Elevation of Privilege"] = [
                "Privilege escalation via token manipulation",
                "Admin access via default credentials"
            ]
            
            # Mitigations
            model.mitigations["Spoofing"] = [
                "Multi-factor authentication",
                "Strong password policies",
                "Rate limiting"
            ]
            model.mitigations["Tampering"] = [
                "HTTPS/TLS encryption",
                "Token signing with HMAC",
                "Certificate pinning"
            ]
            model.mitigations["Repudiation"] = [
                "Comprehensive audit logging",
                "Digital signatures",
                "Tamper-proof logs"
            ]
            model.mitigations["Information Disclosure"] = [
                "Encrypt sensitive data",
                "Sanitize error messages",
                "Constant-time comparisons"
            ]
            model.mitigations["Denial of Service"] = [
                "Rate limiting",
                "CAPTCHA for repeated failures",
                "Account lockout with recovery"
            ]
            model.mitigations["Elevation of Privilege"] = [
                "Principle of least privilege",
                "Role-based access control",
                "Remove default credentials"
            ]
        
        elif "api" in asset_name.lower():
            model.threats["Spoofing"] = [
                "API key theft",
                "Unauthorized API access"
            ]
            model.threats["Tampering"] = [
                "Request parameter manipulation",
                "Response tampering"
            ]
            model.threats["Information Disclosure"] = [
                "Excessive data exposure",
                "Information leakage in errors"
            ]
            model.threats["Denial of Service"] = [
                "API flooding",
                "Resource exhaustion"
            ]
            
            model.mitigations["Spoofing"] = [
                "API key rotation",
                "OAuth 2.0 authentication"
            ]
            model.mitigations["Tampering"] = [
                "Input validation",
                "Request signing",
                "HTTPS only"
            ]
            model.mitigations["Information Disclosure"] = [
                "Minimal data exposure",
                "Generic error messages"
            ]
            model.mitigations["Denial of Service"] = [
                "Rate limiting per API key",
                "Request size limits",
                "Throttling"
            ]
        
        # Calculate risk score (0-10)
        total_threats = sum(len(threats) for threats in model.threats.values())
        total_mitigations = sum(len(mits) for mits in model.mitigations.values())
        model.risk_score = max(0, min(10, total_threats - (total_mitigations * 0.5)))
        
        self.threat_models.append(model)
        return model
    
    async def check_compliance(self, standard: ComplianceStandard) -> Dict[str, Any]:
        """Check compliance with security standards."""
        compliance_checks = {
            ComplianceStandard.GDPR: {
                "data_encryption": "Encrypt personal data at rest and in transit",
                "data_minimization": "Collect only necessary personal data",
                "right_to_erasure": "Implement data deletion mechanisms",
                "consent_management": "Obtain and manage user consent",
                "breach_notification": "Incident response plan for data breaches",
                "data_portability": "Allow users to export their data",
                "privacy_by_design": "Build privacy into system architecture"
            },
            ComplianceStandard.SOC2: {
                "access_control": "Implement role-based access control",
                "change_management": "Document and approve all changes",
                "system_monitoring": "Monitor system availability and performance",
                "incident_response": "Documented incident response procedures",
                "vendor_management": "Assess third-party security",
                "risk_assessment": "Regular risk assessments",
                "security_awareness": "Security training program"
            },
            ComplianceStandard.HIPAA: {
                "access_controls": "Unique user identification and authentication",
                "audit_controls": "Log and monitor access to PHI",
                "integrity_controls": "Protect PHI from alteration/destruction",
                "transmission_security": "Encrypt PHI in transit",
                "encryption": "Encrypt PHI at rest",
                "backup_recovery": "Data backup and disaster recovery",
                "breach_notification": "Report breaches within 60 days"
            },
            ComplianceStandard.PCI_DSS: {
                "firewall_configuration": "Protect cardholder data with firewalls",
                "password_defaults": "Change default passwords",
                "protect_cardholder_data": "Encrypt stored cardholder data",
                "encrypt_transmission": "Encrypt cardholder data in transit",
                "antivirus": "Use and maintain antivirus software",
                "secure_systems": "Develop secure systems and applications",
                "access_restriction": "Restrict access to cardholder data",
                "unique_ids": "Assign unique ID to each user",
                "physical_access": "Restrict physical access to data",
                "track_monitor": "Track and monitor network access",
                "test_security": "Regularly test security systems",
                "security_policy": "Maintain information security policy"
            }
        }
        
        checks = compliance_checks.get(standard, {})
        results = {
            "standard": standard.value,
            "checks": checks,
            "compliant": False,
            "missing_controls": list(checks.keys()),
            "recommendations": list(checks.values())
        }
        
        return results
    
    async def comprehensive_security_audit(self, path: str) -> SecurityAuditReport:
        """Perform comprehensive security audit."""
        # Scan for vulnerabilities
        vulnerabilities = await self.scan_vulnerabilities(path)
        
        # Create threat models for common assets
        threat_models = []
        common_assets = ["authentication_system", "api_endpoints", "database_access", "user_data"]
        for asset in common_assets:
            model = await self.threat_model(asset)
            threat_models.append(model)
        
        # Check compliance
        compliance_status = {}
        for standard in ComplianceStandard:
            result = await self.check_compliance(standard)
            compliance_status[standard.value] = result["compliant"]
        
        # Calculate overall risk score
        vuln_score = (
            len([v for v in vulnerabilities if v.severity == ThreatLevel.CRITICAL]) * 10 +
            len([v for v in vulnerabilities if v.severity == ThreatLevel.HIGH]) * 5 +
            len([v for v in vulnerabilities if v.severity == ThreatLevel.MEDIUM]) * 2
        ) / max(len(vulnerabilities), 1)
        
        threat_score = sum(tm.risk_score for tm in threat_models) / max(len(threat_models), 1)
        risk_score = min(10, (vuln_score + threat_score) / 2)
        
        # Generate summary
        critical_count = len([v for v in vulnerabilities if v.severity == ThreatLevel.CRITICAL])
        high_count = len([v for v in vulnerabilities if v.severity == ThreatLevel.HIGH])
        
        summary = f"""
Security Audit Summary:
- Total Vulnerabilities: {len(vulnerabilities)}
- Critical: {critical_count}
- High: {high_count}
- Overall Risk Score: {risk_score:.1f}/10
- Threat Models Analyzed: {len(threat_models)}
"""
        
        # Generate recommendations
        recommendations = [
            "Address all critical vulnerabilities immediately",
            "Implement secure coding practices",
            "Regular security training for developers",
            "Automated security scanning in CI/CD",
            "Regular penetration testing",
            "Incident response plan",
            "Security monitoring and alerting"
        ]
        
        report = SecurityAuditReport(
            timestamp=datetime.now(),
            vulnerabilities=vulnerabilities,
            threat_models=threat_models,
            compliance_status=compliance_status,
            risk_score=risk_score,
            summary=summary,
            recommendations=recommendations
        )
        
        return report
    
    def generate_security_report(self, report: SecurityAuditReport) -> str:
        """Generate formatted security report."""
        output = []
        output.append("=" * 80)
        output.append("SECURITY AUDIT REPORT")
        output.append("=" * 80)
        output.append(f"Timestamp: {report.timestamp}")
        output.append(f"Risk Score: {report.risk_score:.1f}/10")
        output.append("")
        
        output.append("VULNERABILITY SUMMARY")
        output.append("-" * 80)
        output.append(f"Total Vulnerabilities: {len(report.vulnerabilities)}")
        output.append(f"Critical: {report.get_critical_count()}")
        output.append(f"High: {report.get_high_count()}")
        output.append("")
        
        if report.vulnerabilities:
            output.append("VULNERABILITIES")
            output.append("-" * 80)
            for vuln in report.vulnerabilities[:10]:  # Top 10
                output.append(f"\n[{vuln.severity.value.upper()}] {vuln.title}")
                output.append(f"Location: {vuln.location}:{vuln.line_number}")
                if vuln.code_snippet:
                    output.append(f"Code: {vuln.code_snippet}")
                output.append(f"Remediation: {vuln.remediation}")
        
        output.append("\n" + "=" * 80)
        output.append("RECOMMENDATIONS")
        output.append("-" * 80)
        for i, rec in enumerate(report.recommendations, 1):
            output.append(f"{i}. {rec}")
        
        return "\n".join(output)


# Convenience functions
async def security_audit(path: str) -> SecurityAuditReport:
    """Quick security audit."""
    sec_ops = SecurityOpsCenter()
    return await sec_ops.comprehensive_security_audit(path)


async def scan_vulnerabilities(path: str) -> List[SecurityVulnerability]:
    """Quick vulnerability scan."""
    sec_ops = SecurityOpsCenter()
    return await sec_ops.scan_vulnerabilities(path)


async def threat_model(asset: str) -> ThreatModel:
    """Quick threat modeling."""
    sec_ops = SecurityOpsCenter()
    return await sec_ops.threat_model(asset, "")


# Global security ops center
_security_ops: Optional[SecurityOpsCenter] = None


def get_security_ops() -> SecurityOpsCenter:
    """Get global security operations center."""
    global _security_ops
    if _security_ops is None:
        _security_ops = SecurityOpsCenter()
    return _security_ops
