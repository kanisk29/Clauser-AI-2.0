const form = document.getElementById("contractForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    document.getElementById("loadingSection").style.display = "block";
    document.getElementById("resultsSection").style.display = "none";

    const formData = new FormData();

    formData.append(
        "contract_type",
        document.getElementById("contractType").value
    );

    formData.append(
        "industry",
        document.getElementById("industry").value
    );

    formData.append(
        "persona",
        document.getElementById("persona").value
    );

    const contractFile =
        document.getElementById("contractFile").files[0];

    const playbookFile =
        document.getElementById("playbookFile").files[0];

    if (!contractFile) {

        alert("Please upload a contract.");
        return;
    }

    formData.append(
        "contract_file",
        contractFile
    );

    if (playbookFile) {

        formData.append(
            "playbook_file",
            playbookFile
        );
    }

    try {

        const response = await fetch(
            "https://kanisk29-clauser-ai-backend.hf.space/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        const data =
            result.final_output || result;

        document.getElementById(
            "loadingSection"
        ).style.display = "none";

        document.getElementById(
            "resultsSection"
        ).style.display = "block";

        renderResults(data);

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "loadingSection"
        ).style.display = "none";

        alert("Failed to analyze contract.");
    }
});

function renderResults(data) {

    renderHealthScore(data);

    renderMetrics(data);

    renderExecutiveSummary(data);

    renderPlaybook(data);

    renderCompliance(data);

    renderNegotiations(data);

    renderRisks(data);
}

function renderHealthScore(data) {

    const score =
        data.health_score || 0;

    const scoreElement =
        document.getElementById("healthScore");

    scoreElement.innerText =
        `${score}/100`;

    if (score >= 80) {

        scoreElement.style.color =
            "#16a34a";
    }

    else if (score >= 60) {

        scoreElement.style.color =
            "#f59e0b";
    }

    else {

        scoreElement.style.color =
            "#dc2626";
    }
}


function renderExecutiveSummary(data) {

    document.getElementById(
        "executiveSummary"
    ).innerHTML = `

        <p>
            ${data.executive_summary || "No summary available"}
        </p>

    `;
}

function renderMetrics(data) {

    const risks = data.risks || [];

    const highRisks = risks.filter(
        r => r.risk_level?.toLowerCase() === "high"
    ).length;

    document.getElementById(
        "highRiskCount"
    ).innerText = highRisks;

    document.getElementById(
        "complianceCount"
    ).innerText =
        (data.compliance || []).length;

    document.getElementById(
        "negotiationCount"
    ).innerText =
        (data.negotiations || []).length;
}
function renderPlaybook(data) {

    const container =
        document.getElementById(
            "playbookResults"
        );

    const conflicts =
        data.playbook_conflicts || [];

    if (conflicts.length === 0) {

        container.innerHTML = "";

        return;
    }

    let html = `
        <h3 class="mb-3">
            Playbook Conflicts
        </h3>
    `;

    conflicts.forEach(item => {

        html += `

            <div class="risk-card risk-medium">

                <div class="risk-title">
                    ${item.policy}
                </div>

                <p>
                    ${item.contract_clause}
                </p>

                <strong>
                    Recommendation
                </strong>

                <p>
                    ${item.recommendation}
                </p>

            </div>

        `;
    });

    container.innerHTML = html;
}


function renderCompliance(data) {

    const findings =
        data.compliance || [];

    let html = `
        <h3 class="mb-3">
            Compliance Findings
        </h3>
    `;

    findings.forEach(item => {

        html += `

            <div class="risk-card risk-medium">

                <div class="risk-title">
                    ${item.law}
                </div>

                <p>
                    ${item.issue}
                </p>

                <strong>
                    Severity:
                </strong>

                ${item.severity}

            </div>

        `;
    });

    document.getElementById(
        "complianceResults"
    ).innerHTML = html;
}


function renderNegotiations(data) {

    const negotiations =
        data.negotiations || [];

    let html = `
        <h3 class="mb-3">
            Negotiation Suggestions
        </h3>
    `;

    negotiations.forEach(item => {

        html += `

            <div class="risk-card">

                <div class="risk-title">
                    ${item.clause}
                </div>

                <strong>
                    Suggested Clause
                </strong>

                <p>
                    ${item.proposed_clause}
                </p>

            </div>

        `;
    });

    document.getElementById(
        "negotiationResults"
    ).innerHTML = html;
}


function renderRisks(data) {

    const risks =
        data.risks || [];

    let html = `
        <h3 class="mb-3">
            Risk Findings
        </h3>
    `;

    risks.forEach(risk => {

        const riskClass =
            risk.risk_level.toLowerCase() === "high"
            ? "risk-high"
            : risk.risk_level.toLowerCase() === "medium"
            ? "risk-medium"
            : "risk-low";

        html += `

            <div class="risk-card ${riskClass}">

                <div class="risk-title">

                    ${risk.risk_level} Risk

                </div>

                <h5>
                    ${risk.clause}
                </h5>

                <p>
                    ${risk.explanation}
                </p>

                <strong>
                    Legal Reference
                </strong>

                <p>
                    ${risk.reference}
                </p>

                <strong>
                    Suggested Mitigation
                </strong>

                <p>
                    ${risk.mitigation}
                </p>

            </div>

        `;
    });

    document.getElementById(
        "riskResults"
    ).innerHTML = html;
}
const themeToggle =
    document.getElementById(
        "themeToggle"
    );

const savedTheme =
    localStorage.getItem(
        "theme"
    );

if(savedTheme === "dark") {

    document.body.classList.add(
        "dark-mode"
    );

    themeToggle.innerText = "☀️";
}

themeToggle.addEventListener(
    "click",
    () => {

        document.body.classList.toggle(
            "dark-mode"
        );

        const dark =
            document.body.classList.contains(
                "dark-mode"
            );

        localStorage.setItem(
            "theme",
            dark ? "dark" : "light"
        );

        themeToggle.innerText =
            dark ? "☀️" : "🌙";
    }
);