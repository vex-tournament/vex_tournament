function updateRP(RPInput) {
    let side;
    if (RPInput.id.includes("side1")) {
        side = 1;
    } else {
        side = 2;
    }

    let matchNumber = RPInput.id.split("_")[1];

    // update the hidden input
    document.getElementById("side" + side + "RPHidden_" + matchNumber).value = RPInput.value;
}

function updateCompleted(completedInput) {
    let matchNumber = completedInput.id.split("_")[1];

    // update the hidden input
    document.getElementById("completedHidden_" + matchNumber).value = completedInput.checked;
}

function allianceSelection() {
    // temporary, because there is no use for this page yet
    window.location.href = "/alliance_selection/" + 8;
    return;

    let allianceNumber = prompt("Enter the number of alliances you want to select (1-8): ");

    if (allianceNumber === null) {
        return;
    }

    if ("0123456789".includes(allianceNumber) && allianceNumber !== "" && allianceNumber >= 1 && allianceNumber <= 8) {
        allianceNumber = parseInt(allianceNumber);
    } else {
        alert("Invalid number of alliances.");
        return;
    }

    // redirect to the alliance selection page, passing the number of alliances
    window.location.href = "/alliance_selection/" + allianceNumber;
}

let alliances = {

}

function selectAlliance(team) {
    // get the team's current alliance
    let teamElement = document.getElementById("alliance_" + team)
    let currentAlliance = teamElement.value;

    if (currentAlliance !== "None") {
        // update the alliance's alliance
        let allianceElement = document.getElementById("alliance_" + currentAlliance);
        allianceElement.value = team;

        teamElement.parentElement.parentElement.classList.add("table-success");
        allianceElement.parentElement.parentElement.classList.add("table-success");


        let allianceOptions = document.getElementsByClassName("allianceOption_" + currentAlliance);
        for (let i = 0; i < allianceOptions.length; i++) {
            allianceOptions[i].disabled = true;
        }

        // disable both the current team and the alliance from the list
        let teamOptions = document.getElementsByClassName("allianceOption_" + team);
        for (let i = 0; i < teamOptions.length; i++) {
            teamOptions[i].disabled = true;
        }
    } else {
        teamElement.parentElement.parentElement.classList.remove("table-success");
        // enable the current team
        let teamOptions = document.getElementsByClassName("allianceOption_" + team);
        for (let i = 0; i < teamOptions.length; i++) {
            teamOptions[i].disabled = false;
        }
    }

    // check if the team already has an alliance

    if (alliances[team] !== undefined) {
        // enable the previous alliance
        let previousAlliance = alliances[team];
        let previousAllianceOptions = document.getElementsByClassName("allianceOption_" + previousAlliance);
        for (let i = 0; i < previousAllianceOptions.length; i++) {
            previousAllianceOptions[i].disabled = false;
        }

        // update the previous alliance's alliance
        let prevAllianceElement = document.getElementById("alliance_" + previousAlliance);
        prevAllianceElement.value = "None";
        prevAllianceElement.parentElement.parentElement.classList.remove("table-success")
    }

    delete alliances[alliances[team]]
    delete alliances[team];

    // save the alliance
    if (currentAlliance !== "None") {
        alliances[team] = currentAlliance;
        alliances[currentAlliance] = team;
    }

    // update alliance count
    document.getElementById("alliance-count").innerHTML = "Number of Alliances: " + (Object.keys(alliances).length / 2);

    // undisable the input for team and alliance, because disabled values are not sent to the server
    let currentTeam = document.getElementById("alliance_" + team).options;

    for (let i = 0; i < currentTeam.length; i++) {
        if (currentTeam[i].value === currentAlliance) {
            currentTeam[i].disabled = false;
        }
    }

    // repeat for the alliance
    let currentAllianceOptions = document.getElementById("alliance_" + currentAlliance).options;

    for (let i = 0; i < currentAllianceOptions.length; i++) {
        if (currentAllianceOptions[i].value === team.toString()) {
            currentAllianceOptions[i].disabled = false;
        }
    }
}