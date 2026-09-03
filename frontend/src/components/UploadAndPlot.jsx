import React from 'react';
import axios from 'axios';

export default function UploadAndPlot({onPredictResult}){
  const [file, setFile] = React.useState(null)
  const [preview, setPreview] = React.useState(null)

  function handleFile(e){
    const f = e.target.files[0]
    setFile(f)
    const reader = new FileReader()
    reader.onload = (ev)=>{ setPreview(ev.target.result) }
    reader.readAsText(f)
  }

  async function handleUpload(){
    if(!file) return
    const fd = new FormData()
    fd.append('file', file)
    const res = await axios.post('/api/predict', fd, {headers:{'Content-Type':'multipart/form-data'}})
    onPredictResult(res.data)
  }

  return (
    <div>
      <input type="file" accept=".csv" onChange={handleFile} />
      <button onClick={handleUpload}>Upload & Predict</button>
      {preview && <pre style={{maxHeight:200,overflow:'auto'}}>{preview.slice(0,1000)}</pre>}
    </div>
  )
}
