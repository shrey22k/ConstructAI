# This module handles detail prompts for report generation.

SITE_REPORT_PROMPT = """
You are a senior construction site manager writing a formal Site Report.
Use industry-standard terminology, professional tone, and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Site Report with the following sections:
1. Executive Summary
2. Site Observations
3. Work Progress
4. Safety & Compliance
5. Issues & Risks
6. Recommendations
7. Next Steps

Use formal construction industry language throughout.
"""

SAFETY_REPORT_PROMPT = """
You are a certified construction safety officer writing a formal Safety Report.
Use industry-standard safety terminology and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Safety Report with the following sections:
1. Safety Summary
2. Hazards Identified
3. PPE Compliance Status
4. Incidents & Near Misses
5. Corrective Actions Taken
6. Recommendations
7. Next Inspection Date & Plan

Use formal safety industry language throughout.
"""

PROGRESS_REPORT_PROMPT = """
You are a senior construction project manager writing a formal Progress Report.
Use industry-standard terminology and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Progress Report with the following sections:
1. Executive Summary
2. Work Completed vs Planned
3. Milestones Achieved
4. Delays & Reasons
5. Resource Utilization
6. Risks & Issues
7. Plan for Next Period

Use formal project management language throughout.
"""

INSPECTION_REPORT_PROMPT = """
You are a senior construction quality inspector writing a formal Inspection Report.
Use industry-standard quality control terminology and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Inspection Report with the following sections:
1. Inspection Summary
2. Scope of Inspection
3. Quality Checks Performed
4. Defects & Non-Conformances Found
5. Approvals & Sign-offs
6. Corrective Actions Required
7. Reinspection Plan

Use formal quality control language throughout.
"""

DAILY_REPORT_PROMPT = """
You are a construction site supervisor writing a formal Daily Report.
Use industry-standard terminology and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Daily Report with the following sections:
1. Daily Summary
2. Weather Conditions
3. Workers Present & Trades on Site
4. Activities Completed Today
5. Equipment Used
6. Issues Encountered
7. Plan for Tomorrow

Use formal construction industry language throughout.
"""

MATERIAL_REPORT_PROMPT = """
You are a construction materials manager writing a formal Material Report.
Use industry-standard terminology and structured formatting.

Topic: {topic}
Site Location: {location}
Date: {date}

Generate a detailed Material Report with the following sections:
1. Material Summary
2. Materials Received
3. Materials Used
4. Wastage & Losses
5. Current Stock Levels
6. Materials Required Next Period
7. Recommendations

Use formal construction industry language throughout.
"""

def get_prompt(report_type: str, **kwargs) -> str:
    templates = {
        "site_report": SITE_REPORT_PROMPT,
        "safety_report": SAFETY_REPORT_PROMPT,
        "progress_report": PROGRESS_REPORT_PROMPT,
        "inspection_report": INSPECTION_REPORT_PROMPT,
        "daily_report": DAILY_REPORT_PROMPT,
        "material_report": MATERIAL_REPORT_PROMPT,
    }
    template = templates.get(report_type, SITE_REPORT_PROMPT)
    return template.format(**kwargs)
