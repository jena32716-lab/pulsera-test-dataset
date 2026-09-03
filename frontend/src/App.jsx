import React from 'react';
import UploadAndPlot from './components/UploadAndPlot';
import PredictPanel from './components/PredictPanel';

function App(){
  const [lastResult, setLastResult] = React.useState(null)
  return (
    <div style={{padding:20}}>
      <h2>PPG Health Detector (Demo)</h2>
      <UploadAndPlot onPredictResult={setLastResult} />
      <PredictPanel result={lastResult} />
    </div>
  )
}

export default App;
