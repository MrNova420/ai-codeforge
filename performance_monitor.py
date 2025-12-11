#!/usr/bin/env python3
"""
Performance Monitor - Tracks and reports system performance metrics
Monitors agent execution time, throughput, and resource usage
"""

import time
import psutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque


@dataclass
class PerformanceMetric:
    """Represents a single performance metric."""
    metric_name: str
    value: float
    unit: str
    timestamp: str
    agent: Optional[str] = None
    category: str = "general"


class PerformanceMonitor:
    """
    Monitors and tracks system and agent performance.
    
    Features:
    - Agent execution time tracking
    - Throughput metrics (tasks/minute)
    - Resource usage (CPU, memory)
    - Historical performance data
    - Performance alerts
    """
    
    def __init__(self, history_size: int = 1000):
        """
        Initialize performance monitor.
        
        Args:
            history_size: Number of metrics to keep in history
        """
        self.metrics_history: deque = deque(maxlen=history_size)
        self.agent_metrics: Dict[str, Dict[str, List[float]]] = {}
        self.task_times: Dict[str, List[float]] = {}
        self.start_time = time.time()
        
        # Performance thresholds
        self.thresholds = {
            'task_duration_slow': 60.0,  # seconds
            'task_duration_critical': 180.0,  # seconds
            'memory_warning': 80.0,  # percentage
            'cpu_warning': 90.0  # percentage
        }
        
        # Alerts
        self.alerts = []
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        unit: str,
        agent: Optional[str] = None,
        category: str = "general"
    ):
        """Record a performance metric."""
        metric = PerformanceMetric(
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=datetime.now().isoformat(),
            agent=agent,
            category=category
        )
        
        self.metrics_history.append(metric)
        
        # Check thresholds
        self._check_thresholds(metric)
    
    def start_task_timer(self, task_id: str, agent: str):
        """Start timing a task."""
        if agent not in self.agent_metrics:
            self.agent_metrics[agent] = {
                'durations': [],
                'start_times': {},
                'task_count': 0
            }
        
        self.agent_metrics[agent]['start_times'][task_id] = time.time()
    
    def end_task_timer(self, task_id: str, agent: str) -> float:
        """End timing a task and record duration."""
        if agent not in self.agent_metrics:
            return 0.0
        
        start_times = self.agent_metrics[agent].get('start_times', {})
        if task_id not in start_times:
            return 0.0
        
        duration = time.time() - start_times[task_id]
        
        # Record metrics
        self.agent_metrics[agent]['durations'].append(duration)
        self.agent_metrics[agent]['task_count'] += 1
        del start_times[task_id]
        
        # Record general metric
        self.record_metric(
            metric_name="task_duration",
            value=duration,
            unit="seconds",
            agent=agent,
            category="performance"
        )
        
        return duration
    
    def get_agent_stats(self, agent: str) -> Dict[str, Any]:
        """Get performance statistics for an agent."""
        if agent not in self.agent_metrics:
            return {
                'agent': agent,
                'tasks_completed': 0,
                'avg_duration': 0.0,
                'min_duration': 0.0,
                'max_duration': 0.0,
                'total_time': 0.0
            }
        
        metrics = self.agent_metrics[agent]
        durations = metrics.get('durations', [])
        
        if not durations:
            return {
                'agent': agent,
                'tasks_completed': 0,
                'avg_duration': 0.0,
                'min_duration': 0.0,
                'max_duration': 0.0,
                'total_time': 0.0
            }
        
        return {
            'agent': agent,
            'tasks_completed': metrics.get('task_count', 0),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_time': sum(durations),
            'throughput': len(durations) / ((time.time() - self.start_time) / 60)  # tasks/minute
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall system performance statistics."""
        try:
            # CPU and memory usage
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Calculate overall metrics
            all_durations = []
            total_tasks = 0
            for agent_data in self.agent_metrics.values():
                all_durations.extend(agent_data.get('durations', []))
                total_tasks += agent_data.get('task_count', 0)
            
            uptime = time.time() - self.start_time
            
            return {
                'uptime_seconds': uptime,
                'uptime_formatted': str(timedelta(seconds=int(uptime))),
                'total_tasks': total_tasks,
                'avg_task_duration': sum(all_durations) / len(all_durations) if all_durations else 0.0,
                'throughput': total_tasks / (uptime / 60) if uptime > 0 else 0.0,  # tasks/minute
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_used_mb': memory.used / (1024 * 1024),
                'memory_available_mb': memory.available / (1024 * 1024),
                'active_alerts': len([a for a in self.alerts if not a.get('acknowledged', False)])
            }
        except Exception as e:
            return {
                'error': str(e),
                'uptime_seconds': time.time() - self.start_time,
                'total_tasks': sum(m.get('task_count', 0) for m in self.agent_metrics.values())
            }
    
    def get_all_agent_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get performance stats for all agents."""
        return {
            agent: self.get_agent_stats(agent)
            for agent in self.agent_metrics.keys()
        }
    
    def get_top_performers(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing agents by throughput."""
        all_stats = self.get_all_agent_stats()
        
        # Sort by tasks completed
        sorted_agents = sorted(
            all_stats.items(),
            key=lambda x: x[1].get('tasks_completed', 0),
            reverse=True
        )
        
        return [
            {'agent': agent, **stats}
            for agent, stats in sorted_agents[:limit]
        ]
    
    def get_slow_agents(self, threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """Get agents with slow average execution time."""
        threshold = threshold or self.thresholds['task_duration_slow']
        all_stats = self.get_all_agent_stats()
        
        slow_agents = [
            {'agent': agent, **stats}
            for agent, stats in all_stats.items()
            if stats.get('avg_duration', 0) > threshold
        ]
        
        return sorted(slow_agents, key=lambda x: x['avg_duration'], reverse=True)
    
    def _check_thresholds(self, metric: PerformanceMetric):
        """Check if metric exceeds thresholds and create alerts."""
        if metric.metric_name == "task_duration":
            if metric.value > self.thresholds['task_duration_critical']:
                self._create_alert(
                    severity="critical",
                    message=f"Agent {metric.agent} took {metric.value:.1f}s (>180s threshold)",
                    metric=metric
                )
            elif metric.value > self.thresholds['task_duration_slow']:
                self._create_alert(
                    severity="warning",
                    message=f"Agent {metric.agent} took {metric.value:.1f}s (>60s threshold)",
                    metric=metric
                )
    
    def _create_alert(self, severity: str, message: str, metric: PerformanceMetric):
        """Create a performance alert."""
        alert = {
            'severity': severity,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'metric': {
                'name': metric.metric_name,
                'value': metric.value,
                'agent': metric.agent
            },
            'acknowledged': False
        }
        
        self.alerts.append(alert)
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get performance alerts."""
        if severity:
            return [a for a in self.alerts if a['severity'] == severity]
        return self.alerts
    
    def acknowledge_alert(self, alert_index: int):
        """Acknowledge an alert."""
        if 0 <= alert_index < len(self.alerts):
            self.alerts[alert_index]['acknowledged'] = True
    
    def get_performance_report(self) -> str:
        """Get a formatted performance report."""
        system = self.get_system_stats()
        top = self.get_top_performers(3)
        slow = self.get_slow_agents()
        
        report = f"""
╔════════════════════════════════════════════════════════════╗
║                  Performance Report                         ║
╚════════════════════════════════════════════════════════════╝

System Overview:
  • Uptime: {system['uptime_formatted']}
  • Total Tasks: {system['total_tasks']}
  • Throughput: {system.get('throughput', 0):.2f} tasks/min
  • Avg Duration: {system.get('avg_task_duration', 0):.2f}s
  • CPU Usage: {system.get('cpu_percent', 0):.1f}%
  • Memory: {system.get('memory_percent', 0):.1f}%
  • Active Alerts: {system.get('active_alerts', 0)}

Top Performers:
"""
        
        for i, agent_stat in enumerate(top, 1):
            report += f"  {i}. {agent_stat['agent']}: {agent_stat['tasks_completed']} tasks ({agent_stat['avg_duration']:.1f}s avg)\n"
        
        if slow:
            report += "\nSlow Agents (>60s avg):\n"
            for agent_stat in slow:
                report += f"  • {agent_stat['agent']}: {agent_stat['avg_duration']:.1f}s avg\n"
        
        return report


# Global instance
_monitor_instance = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get or create performance monitor instance."""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = PerformanceMonitor()
    return _monitor_instance
