"""
tools/health.py — Basic hardware & software health checks (PoC)
Provides CPU, memory, disk usage and simple suggestion.
"""
import psutil

def basic_health_report():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    report = (
        f"CPU usage: {cpu}%\n"
        f"Memory: {mem.percent}% used ({round(mem.used/1024**3,1)} GB of {round(mem.total/1024**3,1)} GB)\n"
        f"Disk: {disk.percent}% used ({round(disk.used/1024**3,1)} GB of {round(disk.total/1024**3,1)} GB)\n"
    )
    # add simple suggestions
    suggestions = []
    if cpu > 85:
        suggestions.append("High CPU: consider closing heavy apps or checking for runaway processes.")
    if mem.percent > 85:
        suggestions.append("High memory usage: consider closing apps or increasing virtual memory.")
    if disk.percent > 90:
        suggestions.append("Disk nearly full: consider cleaning temp files or removing large unused files.")
    if suggestions:
        report += "\nSuggestions:\n- " + "\n- ".join(suggestions)
    else:
        report += "\nSystem health appears normal."
    return report