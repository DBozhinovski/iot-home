import React, { Component } from 'react';
import axios from 'axios';
import CssBaseline from '@material-ui/core/CssBaseline';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';

import 'typeface-roboto';

const styles = {
  card: {
    minWidth: 275,
  },
};

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      currentReading: {
        RH: '0 %',
        temp: '0.0 C',
        ALL: '0 lux',
      },
    };
  }

  componentDidMount() {
    this.fetchWeatherData();
    setInterval(async () => {
      this.fetchWeatherData();
    }, 60 * 1000);
  }

  async fetchWeatherData() {
    const res = await axios.get('/status.json');
    this.setState({
      currentReading: res.data,
    });
  }

  render() {
    const { classes } = this.props;

    return (
      <React.Fragment>
        <CssBaseline />
        <Card className={classes.card}>
          <CardHeader
            title="Current temperature"
          />
          <CardContent>
            <Typography>
              {this.state.currentReading.temp}
            </Typography>
          </CardContent>
        </Card>
        <Card className={classes.card}>
          <CardHeader
            title="Current humidity"
          />
          <CardContent>
            <Typography>
              {this.state.currentReading.RH}
            </Typography>
          </CardContent>
        </Card>
        <Card className={classes.card}>
          <CardHeader
            title="Current ambient light"
          />
          <CardContent>
            <Typography>
              {this.state.currentReading.ALL}
            </Typography>
          </CardContent>
        </Card>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(App);
