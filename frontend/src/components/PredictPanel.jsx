import React from 'react';

export default function PredictPanel({result}){
  if(!result) return <div>No prediction yet</div>
  return (
    <div>
      <h3>Prediction result</h3>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  )
}
