import React, { useState, useEffect, useRef } from 'react';
import {FormControl, Button, Grid} from "@material-ui/core";
import { HotTable } from '@handsontable/react';
import 'handsontable/dist/handsontable.full.css';
import ReactSearchBox from 'react-search-box'
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

function ViewTask() {
  const [universityList, setUniversityList] = useState([]);
  const [university, setUniversity] = useState('');
  const [queryResult, setQueryResult] = useState([]);
  const [resultType, setResultType] = useState('');
  let tmp = useRef([]);

  useEffect(() => {
    (async () => {
      try {
          await fetch('/getUniversityWithFacultyFailure').then(res => res.json()).then(data => {
            setUniversityList(data.university);
          });
      } catch (e) {
          console.log(e);
      }
    })();
  }, []);

  async function submitQuery() {
    let q = {'university': university}
    await fetch('/getTask', {method:"POST",body:JSON.stringify(q),headers:{"content_type":"application/json"}})
    .then(async res => res.json()).then( async data => {
      tmp.current = data
      console.log(data.result);
      console.log(tmp);
    });
    setQueryResult(tmp.current.result);
    setResultType(tmp.current.type);
    console.log(resultType, tmp.current.type)
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
        </Grid>
      </form>
      <div>
        <Button color="secondary" onClick={submitQuery}>
            Submit
        </Button>
      </div>
      <HotTable root="hot" 
                data={queryResult} 
                colHeaders={['University', 'Department', 'Execution Time', 'Algo Version', 'Status', 'Time Stamp', 'URL']} 
                columns={[
                  {type: 'text'},
                  {type: 'text'},
                  {type: 'numeric'},
                  {type: 'numeric'},
                  {type: 'text'},
                  {type: 'text'},
                  {type: 'text'}
                ]}
                rowHeaders={true} 
                filters={true} 
                dropdownMenu={true}
                colWidths={[200, 300, 140, 130, 80, 185, 600]}
                className={"htCenter"}
                manualColumnResize={true}
                licenseKey={'non-commercial-and-evaluation'}/>
    </div>
  );
}

export default ViewTask;