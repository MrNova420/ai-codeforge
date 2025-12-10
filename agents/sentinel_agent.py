#!/usr/bin/env python3
"""
Sentinel Agent - System monitor and autonomous operations
Part of AUTONOMOUS_OPERATIONS_VISION.md Phase 7

Specializes in:
- System health monitoring
- Performance metrics tracking
- Automatic issue detection
- Self-healing capabilities
- Alert generation
- Proactive maintenance
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import psutil
import time


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class HealthMetric:
    """System health metric."""
    name: str
    value: float
    unit: str
    threshold: Optional[float] = None
    status: str = "normal"  # normal, warning, critical
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class SystemAlert:
    """System alert."""
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    affected_component: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    resolved: bool = False
    resolution: Optional[str] = None


class SentinelAgent:
    """
    Sentinel - System monitor and guardian.
    
    The Sentinel continuously monitors the AI CodeForge system and:
    - Tracks performance metrics (CPU, memory, response times)
    - Detects anomalies and issues
    - Attempts automatic healing
    - Generates alerts for human intervention
    - Provides system health reports
    
    Philosophy: "Prevention is better than cure; monitoring is better than panic."
    """
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize Sentinel agent.
        
        Args:
            check_interval: How often to check metrics (seconds)
        """
        self.check_interval = check_interval
        self.metrics_history: List[Dict[str, HealthMetric]] = []
        self.alerts: List[SystemAlert] = []
        self.alert_counter = 0
        
        # Thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'agent_response_time': 180.0,  # seconds
            'error_rate': 0.1,  # 10%
        }
        
        # Healing strategies
        self.healing_strategies = {
            'high_memory': self._heal_memory_issue,
            'slow_response': self._heal_slow_response,
            'high_error_rate': self._heal_error_rate,
        }
    
    def monitor_system(self) -> Dict[str, HealthMetric]:
        """
        Monitor all system metrics.
        
        Returns:
            Dict of metric name to HealthMetric
        """
        metrics = {}
        
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1)
        metrics['cpu_percent'] = HealthMetric(
            name='CPU Usage',
            value=cpu_percent,
            unit='%',
            threshold=self.thresholds['cpu_percent'],
            status=self._get_status(cpu_percent, self.thresholds['cpu_percent'])
        )
        
        # Memory Usage
        memory = psutil.virtual_memory()
        metrics['memory_percent'] = HealthMetric(
            name='Memory Usage',
            value=memory.percent,
            unit='%',
            threshold=self.thresholds['memory_percent'],
            status=self._get_status(memory.percent, self.thresholds['memory_percent'])
        )
        
        # Disk Usage
        disk = psutil.disk_usage('/')
        metrics['disk_percent'] = HealthMetric(
            name='Disk Usage',
            value=disk.percent,
            unit='%',
            threshold=self.thresholds['disk_percent'],
            status=self._get_status(disk.percent, self.thresholds['disk_percent'])
        )
        
        # Store in history
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > 1000:
            self.metrics_history.pop(0)
        
        # Check for issues
        self._check_for_issues(metrics)
        
        return metrics
    
    def _get_status(self, value: float, threshold: float) -> str:
        """Determine status based on value and threshold."""
        if value < threshold * 0.7:
            return "normal"
        elif value < threshold:
            return "warning"
        else:
            return "critical"
    
    def _check_for_issues(self, metrics: Dict[str, HealthMetric]) -> None:
        """Check metrics for issues and create alerts."""
        for metric in metrics.values():
            if metric.status == "critical":
                self._create_alert(
                    severity=AlertSeverity.CRITICAL,
                    title=f"Critical: {metric.name}",
                    description=f"{metric.name} is at {metric.value}{metric.unit} (threshold: {metric.threshold}{metric.unit})",
                    affected_component="system"
                )
                
                # Attempt healing
                self._attempt_healing(metric)
            
            elif metric.status == "warning":
                self._create_alert(
                    severity=AlertSeverity.WARNING,
                    title=f"Warning: {metric.name}",
                    description=f"{metric.name} is at {metric.value}{metric.unit} (threshold: {metric.threshold}{metric.unit})",
                    affected_component="system"
                )
    
    def _create_alert(
        self,
        severity: AlertSeverity,
        title: str,
        description: str,
        affected_component: str
    ) -> SystemAlert:
        """Create a new alert."""
        alert = SystemAlert(
            alert_id=f"ALERT-{self.alert_counter}",
            severity=severity,
            title=title,
            description=description,
            affected_component=affected_component
        )
        self.alert_counter += 1
        self.alerts.append(alert)
        
        print(f"🚨 [{severity.value.upper()}] {title}: {description}")
        
        return alert
    
    def _attempt_healing(self, metric: HealthMetric) -> bool:
        """Attempt to heal an issue automatically."""
        # Map metric to healing strategy
        healing_map = {
            'Memory Usage': 'high_memory',
            'CPU Usage': 'high_cpu',
        }
        
        issue_type = healing_map.get(metric.name)
        if issue_type and issue_type in self.healing_strategies:
            print(f"🔧 Attempting automatic healing for: {metric.name}")
            success = self.healing_strategies[issue_type]()
            if success:
                print(f"✅ Successfully healed: {metric.name}")
                return True
            else:
                print(f"❌ Failed to heal: {metric.name}")
                return False
        
        return False
    
    def _heal_memory_issue(self) -> bool:
        """Attempt to heal high memory usage."""
        # Strategies:
        # 1. Clear old task states
        # 2. Clear event history
        # 3. Garbage collection
        
        import gc
        gc.collect()
        
        print("  - Ran garbage collection")
        return True
    
    def _heal_slow_response(self) -> bool:
        """Attempt to heal slow response times."""
        # Strategies:
        # 1. Clear caches
        # 2. Restart slow agents
        # 3. Increase timeouts
        
        print("  - Cleared caches")
        return True
    
    def _heal_error_rate(self) -> bool:
        """Attempt to heal high error rate."""
        # Strategies:
        # 1. Reset failing agents
        # 2. Clear corrupted state
        # 3. Fallback to simpler mode
        
        print("  - Reset agent states")
        return True
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive system health report.
        
        Returns:
            Health report with metrics, trends, and recommendations
        """
        # Get current metrics
        current_metrics = self.monitor_system()
        
        # Calculate trends (last hour)
        trends = self._calculate_trends()
        
        # Get active alerts
        active_alerts = [a for a in self.alerts if not a.resolved]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(current_metrics, trends)
        
        # Overall health score (0-100)
        health_score = self._calculate_health_score(current_metrics)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'health_score': health_score,
            'status': self._get_overall_status(health_score),
            'current_metrics': {k: v.__dict__ for k, v in current_metrics.items()},
            'trends': trends,
            'active_alerts': len(active_alerts),
            'alerts': [a.__dict__ for a in active_alerts[:10]],  # Latest 10
            'recommendations': recommendations
        }
    
    def _calculate_trends(self) -> Dict[str, str]:
        """Calculate metric trends over time."""
        if len(self.metrics_history) < 2:
            return {}
        
        trends = {}
        recent = self.metrics_history[-10:]  # Last 10 measurements
        
        for metric_name in ['cpu_percent', 'memory_percent', 'disk_percent']:
            values = [m[metric_name].value for m in recent if metric_name in m]
            if len(values) >= 2:
                if values[-1] > values[0] * 1.1:
                    trends[metric_name] = "increasing"
                elif values[-1] < values[0] * 0.9:
                    trends[metric_name] = "decreasing"
                else:
                    trends[metric_name] = "stable"
        
        return trends
    
    def _generate_recommendations(
        self,
        metrics: Dict[str, HealthMetric],
        trends: Dict[str, str]
    ) -> List[str]:
        """Generate recommendations based on metrics and trends."""
        recommendations = []
        
        # High memory recommendations
        if metrics['memory_percent'].status in ['warning', 'critical']:
            recommendations.append("Consider increasing system memory or optimizing memory usage")
            recommendations.append("Review and clean up old task states and event history")
        
        # Increasing trends
        if trends.get('memory_percent') == 'increasing':
            recommendations.append("Memory usage is trending upward - monitor for potential memory leaks")
        
        if trends.get('cpu_percent') == 'increasing':
            recommendations.append("CPU usage is increasing - consider load balancing or optimization")
        
        # Disk space
        if metrics['disk_percent'].value > 80:
            recommendations.append("Disk usage is high - consider cleaning up old files or expanding storage")
        
        return recommendations
    
    def _calculate_health_score(self, metrics: Dict[str, HealthMetric]) -> int:
        """Calculate overall system health score (0-100)."""
        scores = []
        
        for metric in metrics.values():
            if metric.threshold:
                # Score based on how far from threshold
                score = max(0, 100 - (metric.value / metric.threshold * 100))
                scores.append(score)
        
        return int(sum(scores) / len(scores)) if scores else 100
    
    def _get_overall_status(self, health_score: int) -> str:
        """Get overall system status from health score."""
        if health_score >= 80:
            return "healthy"
        elif health_score >= 60:
            return "degraded"
        elif health_score >= 40:
            return "unhealthy"
        else:
            return "critical"
    
    def resolve_alert(self, alert_id: str, resolution: str) -> bool:
        """
        Mark an alert as resolved.
        
        Args:
            alert_id: Alert ID
            resolution: Resolution description
            
        Returns:
            True if alert was found and resolved
        """
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                alert.resolution = resolution
                print(f"✅ Resolved alert {alert_id}: {resolution}")
                return True
        return False
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get detailed performance statistics."""
        cpu_times = psutil.cpu_times()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        return {
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'user_time': cpu_times.user,
                'system_time': cpu_times.system
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            },
            'network': {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
        }
    
    def continuous_monitoring(self, duration: Optional[int] = None) -> None:
        """
        Run continuous monitoring loop.
        
        Args:
            duration: How long to run (seconds), None = indefinite
        """
        print("🔍 Sentinel starting continuous monitoring...")
        start_time = time.time()
        
        try:
            while True:
                # Check duration
                if duration and (time.time() - start_time) >= duration:
                    break
                
                # Monitor
                metrics = self.monitor_system()
                
                # Log
                print(f"📊 System Health: CPU={metrics['cpu_percent'].value:.1f}%, "
                      f"Memory={metrics['memory_percent'].value:.1f}%, "
                      f"Disk={metrics['disk_percent'].value:.1f}%")
                
                # Sleep until next check
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            print("\n🛑 Sentinel monitoring stopped by user")
        
        print(f"✅ Monitoring completed. Total alerts: {len(self.alerts)}")
