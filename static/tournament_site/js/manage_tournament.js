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