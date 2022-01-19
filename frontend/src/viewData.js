import React, { useState, useEffect, useRef } from 'react';
import {FormControl, Button, Grid} from "@material-ui/core";
import ReactSearchBox from 'react-search-box'
import { HotTable } from '@handsontable/react';
import Chart from "react-google-charts";
import 'handsontable/dist/handsontable.full.css';
import './viewData.css'

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

function ViewData() {
  const [universityList, setUniversityList] = useState([]);
  const [university, setUniversity] = useState('');
  const [departmentList, setDepartmentList] = useState([]);
  const [department, setDepartment] = useState('');
  const [queryResult, setQueryResult] = useState([]);
  const [tableTitle, setTableTitle] = useState('');
  const [sourceURL, setSourceURL] = useState('');
  const [executionTime, setExecutionTime] = useState('?');
  const [taskID, setTaskID] = useState('');

  const[universityFacultyTasks, setUniversityFacultyTasks] = useState([['Status', 'Num']]);
  const[universityFacultyNum, setUniversityFacultyNum] = useState([['Status', 'Num']]);
  const[departmentWithMostFaculty, setDepartmentWithMostFaculty] = useState([['Status', 'Num']]);

  let tmp = useRef([]);

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

  async function submitQuery() {
    let q = {'university': university, 'department': department}
    await fetch('/submitQuery', {method:"POST",body:JSON.stringify(q),headers:{"content_type":"application/json"}})
    .then(async res => res.json()).then( async data => {
      tmp.current = data
      console.log(data.result);
      console.log(tmp);
    });
    setQueryResult(tmp.current.result);
    setTaskID(tmp.current.task_id);
    if (tmp.current.type === 'Faculty') {
      setTableTitle(university + ' - ' + department + ' - ' + tmp.current.type);
    } else {
      setTableTitle(university + ' - ' + tmp.current.type);
    }
    setSourceURL(tmp.current.url);
    setExecutionTime(tmp.current.execution_time);

    let q2 = {'university': university};
    await fetch('/getDetailedStatisticsOfUniversity', {method:"POST",body:JSON.stringify(q2),headers:{"content_type":"application/json"}})
    .then(async res => res.json()).then( async data => {
      setUniversityFacultyTasks(data.table1);
      setUniversityFacultyNum(data.table2);
      setDepartmentWithMostFaculty(data.table3);
    });
  }

  async function changeData() {
    let q = {'id': taskID, 'data': queryResult}
    await fetch('/changeData', {method:"POST",body:JSON.stringify(q),headers:{"content_type":"application/json"}})
    console.log(taskID);
    console.log(queryResult);
  }

  async function correction(change) {
    await fetch('/correction', {method:"POST",body:JSON.stringify(change),headers:{"content_type":"application/json"}})
  }

  return (
    <div>
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
      <div>
        <Button color="secondary" onClick={submitQuery}>
            Submit
        </Button>
      </div>

      <div class="row">
        <div class="column">
          <Chart
            width={'330px'}
            height={'300px'}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={universityFacultyTasks}
            options={{
              title: 'Faculty Task Execution Time',
            }}
          />
        </div>
        <div class="column">
          <Chart
            width={'330px'}
            height={'300px'}
            chartType="PieChart"
            loader={<div>Loading Chart</div>}
            data={universityFacultyNum}
            options={{
              title: 'Faculty Number of Departments',
            }}
          />
        </div>
        <div class="column">
          <Chart
            width={'500px'}
            height={'300px'}
            chartType="Bar"
            loader={<div>Loading Chart</div>}
            data={departmentWithMostFaculty}
            options={{
              chart: {
                title: 'Department with most Faculty'
              },
            }}
          />
        </div>
      </div>

      <div>
        <div># Rows: {queryResult.length}</div>
        <div>Execution Time: {executionTime} Seoncds</div>
        <div>URL: {sourceURL}</div>
        <h2 id='title'>{tableTitle}</h2>
        <div>
          <Button color="secondary" onClick={changeData}>
              change
          </Button>
        </div>
        <HotTable root="hot" 
                data={queryResult} 
                colHeaders={['Name', 'Position', 'Research', 'Email', 'Phone']}
                rowHeaders={true} 
                filters={true} 
                dropdownMenu={true}
                colWidths={[200, 340, 450, 200, 200]}
                className={"htCenter"}
                manualColumnResize={true}
                afterChange={(changes) => {
                  console.log(changes)
                  correction(changes)
                }}
                licenseKey={'non-commercial-and-evaluation'}/>
      </div>
    </div>
  );
}

export default ViewData;