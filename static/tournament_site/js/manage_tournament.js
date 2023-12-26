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