function connect(start, end) {
  // connects the start and end playoff boxes with an arrow
  let startElement = document.getElementById("playoff" + start);
  let endElement = document.getElementById("playoff" + end);



  let startElementRect = startElement.getBoundingClientRect();
  let endElementRect = endElement.getBoundingClientRect();

  if (end === 7) {
    // the winner box should be the same size as the final box
    endElement.style.width = startElementRect.width + "px";
    endElement.style.height = startElementRect.height + "px";

    endElementRect = endElement.getBoundingClientRect();
  }

  let startX = startElementRect.right;
  let startY = startElementRect.top + (startElementRect.height / 2);

  let endX = endElementRect.left;
  let nearEndX = (endX - startX) * 0.7 + startX; // move the end to the left a bit
  let endY = endElementRect.top + (endElementRect.height / 2);

  // draw a line from the start to the end, maintaining the same y value
  let hline1 = document.createElement("div");
  hline1.style.position = "absolute";
  hline1.style.left = startX + "px";
  hline1.style.top = startY + "px";
  hline1.style.width = (nearEndX - startX) + "px";
  hline1.style.height = "0px";
  hline1.style.borderBottom = "1px solid black";

  // draw a line from the previous line to the correct Y value
  let vline = document.createElement("div");
  vline.style.position = "absolute";
  vline.style.left = (startX + (nearEndX - startX)) + "px";
  vline.style.width = "0px";
  vline.style.height = Math.abs(endY - startY) + "px";
  vline.style.borderLeft = "1px solid black";

  if (endY < startY) {
    vline.style.top = endY + "px";
  } else {
    vline.style.top = startY + "px";
  }

  // draw a line from the previous line to the end
  let hline2 = document.createElement("div");
  hline2.style.position = "absolute";
  hline2.style.left = nearEndX + "px";
  hline2.style.top = endY + "px";
  hline2.style.width = (endX - nearEndX) + "px";
  hline2.style.height = "0px";
  hline2.style.borderBottom = "1px solid black";


  document.body.appendChild(hline1);
  document.body.appendChild(vline);
  document.body.appendChild(hline2);
}

document.addEventListener("DOMContentLoaded", (event) => {
  connect(0, 4);
  connect(1, 4);
  connect(2, 5);
  connect(3, 5);
  connect(4, 6);
  connect(5, 6);
  connect(6, 7);
});
