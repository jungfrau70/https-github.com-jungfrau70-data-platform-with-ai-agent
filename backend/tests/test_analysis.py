import pytest
import pandas as pd
import io
import pickle
from fastapi import UploadFile
from app.services.analysis_service import analysis_service

@pytest.mark.asyncio
async def test_process_upload_csv():
    # Setup
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    
    file = UploadFile(filename="test.csv", file=csv_buffer)
    
    # Execute
    summary = await analysis_service.process_upload(file)
    
    # Assert
    assert summary["shape"] == (2, 2)
    assert "col1" in summary["columns"]

@pytest.mark.asyncio
async def test_process_upload_pickle():
    # Setup
    df = pd.DataFrame({'col1': [10, 20], 'col2': ['a', 'b']})
    pkl_buffer = io.BytesIO()
    pd.to_pickle(df, pkl_buffer)
    pkl_buffer.seek(0)
    
    file = UploadFile(filename="test.pkl", file=pkl_buffer)
    
    # Execute
    summary = await analysis_service.process_upload(file)
    
    # Assert
    assert summary["shape"] == (2, 2)
    assert "col1" in summary["columns"]
