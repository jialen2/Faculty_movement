import React, { useState, useEffect } from 'react';
import Chart from "react-google-charts";
import ReactSearchBox from 'react-search-box';
import {FormControl, Button, Grid} from "@material-ui/core";
import { HotTable } from '@handsontable/react';
import "./overView.css";


const parseSearchBoxData = (data) => {
  var records = [];
  for (var i = 0; i < data.length; i++) {
      records.push({"key": data[i], "value":data[i]});
  }
  return records;
}

const SearchBox = ({ placeholder, data, setter, focus }) => {
  return (
      <div className="homeInput">
          <ReactSearchBox
            placeholder={placeholder}
            data={data}
            fuseConfigs={{threshold: 0.05}}
            value=""
            onFocus={(e) => e.target.value=""} 
            onSelect={(e) => setter(e.key)}
          />
      </div>
  )
}


function OverView() {
  const [averageRunningTime, setAverageRunningTime] = useState([0, 0]);
  const [departmentOverview, setDepartmentOverview] = useState([['Status', 'Num']]);
  const [facultyOverview, setFacultyOverview] = useState([['Status', 'Num']]);
  const [departmentExecutionTime, setDepartmentExecutionTime] = useState([['Status', 'Num']]);
  const [facultyExecutionTime, setFacultyExecutionTime] = useState([['Status', 'Num']]);

  const [universityList, setUniversityList] = useState([]);
  const [university, setUniversity] = useState('');
  const [departmentList, setDepartmentList] = useState([]);
  const [department, setDepartment] = useState('');

  const [nextTasks, setNextTasks] = useState([]);
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetch('/averageRunningTime').then(res => res.json()).then(data => {
      setAverageRunningTime([data.department, data.faculty]);
    });
  }, []);

  useEffect(() => {
    fetch('/departmentOverview').then(res => res.json()).then(data => {
      setDepartmentOverview(data.res);
    });
  }, []);

  useEffect(() => {
    fetch('/facultyOverview').then(res => res.json()).then(data => {
      setFacultyOverview(data.res);
    });
  }, []);

  useEffect(() => {
    fetch('/departmentExecutionTime').then(res => res.json()).then(data => {
      setDepartmentExecutionTime(data.res);
    });
  }, []);

  useEffect(() => {
    fetch('/facultyExecutionTime').then(res => res.json()).then(data => {
      setFacultyExecutionTime(data.res);
    });
  }, []);

  useEffect(() => {
    let q = {'page': page, 'university': university, 'department': department}
    fetch('/getNextTasks', {method:"POST",body:JSON.stringify(q),headers:{"content_type":"application/json"}}).then(res => res.json()).then(data => {
      setNextTasks(data.res);
    });
  }, [page]);

  useEffect(() => {
    (async () => {
      try {
          await fetch('/getUniversityList').then(res => res.json()).then(data => {
            setUniversityList(data.university);
          });
      } catch (e) {
          console.log(e);
      }
    })();
  }, []);

  useEffect(() => {
    (async () => {
      try {
          await fetch('/getDepartmentList', {method:"POST",body:JSON.stringify(university),headers:{"content_type":"application/json"}})
          .then(res => res.json()).then(data => {
            setDepartmentList(data.department);
          });
      } catch (e) {
          console.log(e);
      }
    })();
  }, [university]);

  async function prioritize() {
    // let q = {'university': university, 'department': department};
    let q = {'table': nextTasks}
    await fetch('/prioritizeTasks', {method:"POST", body:JSON.stringify(q), headers:{"content_type":"application/json"}})
    let q1 = {'page': page, 'university': university, 'department': department}
    await fetch('/getNextTasks', {method:"POST",body:JSON.stringify(q1),headers:{"content_type":"application/json"}}).then(res => res.json()).then(data => {
      setNextTasks(data.res);
    });
  }

  async function prioritizeAll() {
    let q = {'university': university, 'department': department};
    await fetch('/prioritizeAll', {method:"POST", body:JSON.stringify(q), headers:{"content_type":"application/json"}})
    let q1 = {'page': page, 'university': university, 'department': department}
    await fetch('/getNextTasks', {method:"POST",body:JSON.stringify(q1),headers:{"content_type":"application/json"}}).then(res => res.json()).then(data => {
      setNextTasks(data.res);
    });
  }

  async function deleteTask() {
    let q = {'university': university, 'department': department};
    await fetch('/deleteTasks', {method:"POST", body:JSON.stringify(q), headers:{"content_type":"application/json"}})
  }

  async function refreshTable() {
    setPage(1);
    let q1 = {'page': page, 'university': university, 'department': department}
    await fetch('/getNextTasks', {method:"POST",body:JSON.stringify(q1),headers:{"content_type":"application/json"}}).then(res => res.json()).then(data => {
      setNextTasks(data.res);
    });
  }

  function previousPage(x) {
    if (page > 1 && x === 1) {
      setPage(page - 1);
    } 
    if (x === 2) {
      setPage(page + 1);
    }
  }

  return (
    <div>
      <div class="row">
        <div class="column">
        <Chart
          width={'330px'}
          height={'300px'}
          chartType="PieChart"
          loader={<div>Loading Chart</div>}
          data={departmentOverview}
          options={{
            title: 'Department Task',
          }}
        />
        </div>
        <div class="column">
          <Chart
            width={'330px'}
            height={'300px'}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={facultyOverview}
            options={{
              title: 'Faculty Task',
            }}
          />
        </div>
        <div class="column">
          <Chart
            width={'330px'}
            height={'300px'}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={departmentExecutionTime}
            options={{
              title: `Department Task Execution Time \n(Avg ${averageRunningTime[0]} seconds)`
            }}
          />
        </div>
        <div class="column">
          <Chart
            width={'330px'}
            height={'300px'}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={facultyExecutionTime}
            options={{
              title: `Faculty Task Execution Time \n(Avg ${averageRunningTime[1]} seconds)`
            }}
          />
        </div>
      </div>
      <form>
        <Grid container spacing={2}>
          &nbsp;&nbsp;&nbsp;
          <Grid item xs={4}>
              <FormControl color={'secondary'} fullWidth required>
              <SearchBox placeholder="University" data={parseSearchBoxData(universityList)} setter={setUniversity}/>
              </FormControl>
          </Grid>
          <Grid item xs={4}>
              <FormControl color={'secondary'} fullWidth required>
              <SearchBox placeholder="Department" data={parseSearchBoxData(departmentList)} setter={setDepartment}/>
              </FormControl>
          </Grid>
        </Grid>
      </form>
      <br/>
      <div>
        <Button color="secondary" onClick={refreshTable}>
          Refresh Task Table
        </Button>
      </div>
      <div>
        <Button color="secondary" onClick={() => previousPage(1)}>
          Pre
        </Button>
          {page}
        <Button color="secondary" onClick={() => previousPage(2)}>
          Next
        </Button>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <Button color="secondary" onClick={prioritize}>
          Prioritize
        </Button>
        <Button color="secondary" onClick={prioritizeAll}>
          Prioritize All
        </Button>
      </div>
      <HotTable root="hot" 
                data={nextTasks} 
                colHeaders={['University', 'Department', '']}
                columns={[
                  {type: 'text'},
                  {type: 'text'},
                  {type: 'checkbox'}
                ]}
                rowHeaders={true}
                colWidths={[500, 600]}
                className={"htCenter"}
                manualColumnResize={true}
                licenseKey={'non-commercial-and-evaluation'}/>
    </div>
  );
}

export default OverView;