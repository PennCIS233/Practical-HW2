import { Card, ListGroup, Container } from "react-bootstrap";
import "chart.js/auto";
import { Chart } from "react-chartjs-2";

/*
 * Props:
 *  - appID (string): id of the election
 *  - currVotes (list of integers): number of votes for each choice
 *  - state (JSON): global state of the election
 */
function ElectionInfoCard(props) {
  // list of colors to include in the pie chart
  const colorList = [
    "#3181ba",
    "#632656",
    "#4dc8e9",
    "#45134c",
    "#793ea8",
    "#5ce3fe",
    "#4e0d4d",
    "#2379a8",
    "#142d6a",
  ];

  // JSON of data for the pie chart (in the specified format)
  const data = {
    labels: props.state["VoteOptions"]
      ? props.state["VoteOptions"].split(",")
      : [],
    datasets: [
      {
        label: "Vote Count",
        data: props.currVotes,
        backgroundColor: colorList.slice(0, props.currVotes.length),
        hoverOffset: 4,
        radius: "75%",
      },
    ],
  };

  /*
   * Render the card with a list of election info, as well as a pie chart
   * with the number of votes for each choice.
   */
  return (
    <Card className="h-100">
      <Card.Body>
        <Card.Title>Election Info</Card.Title>
        <ListGroup>
          <ListGroup.Item>
            <b>Creator Address: </b>
            {props.state["Creator"] ? props.state["Creator"] : ""}
          </ListGroup.Item>
          <ListGroup.Item>
            <b>Last Round to Vote: </b>
            {props.state["ElectionEnd"]}
          </ListGroup.Item>
          <ListGroup.Item>
            <b>Vote Options:</b> {props.state["VoteOptions"]}
          </ListGroup.Item>
          <ListGroup.Item>
            <b> Number of Voters:</b>{" "}
            {(props.currVotes &&
              Object.values(props.currVotes).reduce((a, b) => a + b, 0)) ||
              "0"}
          </ListGroup.Item>
        </ListGroup>
        {props.currVotes.reduce((a, b) => a + b, 0) > 0 && (
          <Container className="mt-3 px-5">
            <Chart type="pie" data={data} />
          </Container>
        )}
      </Card.Body>
    </Card>
  );
}

export default ElectionInfoCard;
