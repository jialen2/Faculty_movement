import React, { useState } from 'react';
import './App.css';
import Tabs from 'react-bootstrap/Tabs';
import Tab from 'react-bootstrap/Tab';
import 'bootstrap/dist/css/bootstrap.min.css';
import Overview from './overView';
import ViewData from './viewData';
import ViewTask from './viewTask';

function App() {
  const [tabKey, setTabKey] = useState('overview');

  return (
    <div>
    <Tabs
      id="controlled-tab-example"
      activeKey={tabKey}
      onSelect={(k) => setTabKey(k)}
    >
      <Tab eventKey="overview" title="Overview">
        <Overview/>
      </Tab>
      <Tab eventKey="data" title="Data">
        <ViewData/>
      </Tab>
      <Tab eventKey="failure" title="Tasks">
        <ViewTask/>
      </Tab>
    </Tabs>
    </div>
  );
}

export default App;
