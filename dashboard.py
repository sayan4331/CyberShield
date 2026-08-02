from pydantic import BaseModel


class DashboardSummary(BaseModel):
    """
    Summary statistics displayed on the dashboard.
    """

    total_password_checks: int
    total_url_scans: int
    total_file_scans: int

    safe_urls: int
    dangerous_urls: int

    weak_passwords: int
    medium_passwords: int
    strong_passwords: int

    safe_files: int
    malicious_files: int

    class Config:
        from_attributes = True


class PasswordChart(BaseModel):
    weak: int
    medium: int
    strong: int


class URLChart(BaseModel):
    safe: int
    dangerous: int


class MalwareChart(BaseModel):
    safe: int
    malicious: int


class DashboardCharts(BaseModel):
    """
    Chart data for the dashboard.
    """

    password_strength: PasswordChart
    url_scans: URLChart
    malware_scans: MalwareChart