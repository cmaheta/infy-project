import React, {useState} from 'react';
import ReactDOM from 'react-dom';
import Button from "@mui/material/Button";
import Typography from '@mui/material/Typography';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Box from '@mui/material/Box';
const App = () => {
    const [jobId, setJobId] = useState(10);
    const [jobStatus, setJobStatus] = useState("");
    const handleChange = (event: SelectChangeEvent) => {
        setJobId(event.target.value);
    };
    const handleClick = () => {
        fetch('http://localhost:5000/run-script')
            .then(response => response.json())
            .then(data => {
                alert(data.output);
            })
            .catch(error => console.error('Error:', error));
    };

    return (
        <div>
            <h1>
            <Typography  variant="h6"
                         sx={{
                             color: 'blue',
                             fontWeight: 'bold',
                             padding: '10px',
                             backgroundColor: 'dark blue'
                         }}
                         component="label" >
                Python Script Executor
            </Typography>
            </h1>
            <Box sx={{ width: 250 }}>
            <h1>
            <InputLabel id="demo-simple-select-label">Job To Run</InputLabel>
            </h1>
            <h1>
            <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={jobId}
                label="Job Id"
                onChange={handleChange}
            >
                <MenuItem value={10}>Job with id 10</MenuItem>
                <MenuItem value={20}>Job with id 20</MenuItem>
                <MenuItem value={30}>Job with id 30</MenuItem>
            </Select>
            </h1>
            <Button xs={12} sx={{justifyContent: 'center',alignItems: 'center', height: '53px'}}
                    variant="contained" size="x-large"
                    onClick={handleClick}>Execute Python Script</Button>
            </Box>
        </div>
    );
};

// Render the React component
ReactDOM.render(<App />, document.getElementById('root'));