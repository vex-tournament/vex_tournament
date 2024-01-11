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

let positions = {

}

function selectAlliance(team) {
    // get the team's current alliance
    let teamElement = document.getElementById("alliance_" + team)
    let currentAlliance = teamElement.value;
    let teamPosition = document.getElementById(team + "_position").value;

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

        // set the alliance's position to the team's position
        document.getElementById(currentAlliance + "_position").value = teamPosition;
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

        // change the previous alliance's position to None
        document.getElementById(previousAlliance + "_position").value = "None";

        delete positions[previousAlliance]
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

    // change the position
    changePos(team);
}

function changePos(team) {
    let position = document.getElementById(team + "_position").value;
    let alliance = alliances[team];

    // undisable the past position
    let pastPosition = positions[team];
    let pastPositionOptions = document.getElementsByClassName("positionOption_" + pastPosition);

    for (let i = 0; i < pastPositionOptions.length; i++) {
        pastPositionOptions[i].disabled = false;
    }

    if (alliance !== undefined) {
        // set the alliance's position to the team's position
        document.getElementById(alliance + "_position").value = position;
    }

    if (position === "None") {
        // undisable the past position
        let pastPosition = positions[team];
        let pastPositionOptions = document.getElementsByClassName("positionOption_" + pastPosition);

        for (let i = 0; i < pastPositionOptions.length; i++) {
            pastPositionOptions[i].disabled = false;
        }

        delete positions[team];
        delete positions[alliance];

        return;
    } else {
        positions[team] = position;

        if (alliance !== undefined) {
            positions[alliance] = position;
        }
    }

    // disable the team's position
    let positionOptions = document.getElementsByClassName("positionOption_" + position);

    for (let i = 0; i < positionOptions.length; i++) {
        positionOptions[i].disabled = true;
    }

    // undisable the input for team and alliance, because disabled values are not sent to the server
    let currentTeam = document.getElementById(team + "_position").options;

    for (let i = 0; i < currentTeam.length; i++) {
        if (currentTeam[i].value === position) {
            currentTeam[i].disabled = false;
        }
    }

    // repeat for the alliance
    let currentAllianceOptions = document.getElementById(alliance + "_position").options;

    for (let i = 0; i < currentAllianceOptions.length; i++) {
        if (currentAllianceOptions[i].value === position) {
            currentAllianceOptions[i].disabled = false;
        }
    }
}


document.addEventListener("DOMContentLoaded", (event) => {
    // get the scoreboard table
    let scoreboardTable = document.getElementById("scoreboard");

    if (scoreboardTable !== null) {
        // get the number of teams
        let teamNumber = scoreboardTable.rows.length - 1;

        if (teamNumber > 20) {
            // move the rest of the teams to a new column
            let overflowedTeams = [];

            for (let i = 21; i <= teamNumber; i++) {
                overflowedTeams.push(scoreboardTable.rows[i].innerHTML);
            }

            // add 3 columns to the table
            scoreboardTable.rows[0].innerHTML += "<th>Rank</th><th>Team</th><th>RP</th>";

            // remove the overflowed teams
            for (let i = 21; i <= teamNumber; i++) {
                scoreboardTable.deleteRow(21);
            }

            // readd the overflowed teams, but in the same rows as the first 20 teams
            for (let i = 0; i < overflowedTeams.length; i++) {
                scoreboardTable.rows[i + 1].innerHTML += overflowedTeams[i];
            }
        }
    }
});