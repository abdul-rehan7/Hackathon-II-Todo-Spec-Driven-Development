// frontend/src/app/api/auth/[...path]/route.js
import { NextResponse } from 'next/server';

export async function POST(request, { params }) {
  const { path } = params; // This will be an array like ['register'], ['login'], etc.
  const endpoint = Array.isArray(path) ? path.join('/') : path;

  // Construct the backend URL - the path is already what comes after /api/auth/
  const backendUrl = `http://localhost:8000/api/v1/auth/${endpoint}`;

  try {
    // Check content type to determine how to handle the body
    const contentType = request.headers.get('content-type') || '';

    let response;
    if (contentType.includes('multipart/form-data')) {
      // Handle FormData (for login/register which use FormData)
      const formData = await request.formData();
      response = await fetch(backendUrl, {
        method: 'POST',
        body: formData, // Send the FormData directly
      });
    } else {
      // Handle JSON data
      const body = await request.json();
      response = await fetch(backendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });
    }

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function GET(request, { params }) {
  const { path } = params;
  const endpoint = Array.isArray(path) ? path.join('/') : path;

  // Construct the backend URL
  const backendUrl = `http://localhost:8000/api/v1/auth/${endpoint}`;

  try {
    // Get authorization header if present
    const authHeader = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        ...(authHeader ? { 'authorization': authHeader } : {}),
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy GET error:', error);
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function PUT(request, { params }) {
  const { path } = params;
  const endpoint = Array.isArray(path) ? path.join('/') : path;
  const body = await request.json();

  // Construct the backend URL
  const backendUrl = `http://localhost:8000/api/v1/auth/${endpoint}`;

  try {
    const response = await fetch(backendUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy PUT error:', error);
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function DELETE(request, { params }) {
  const { path } = params;
  const endpoint = Array.isArray(path) ? path.join('/') : path;

  // Construct the backend URL
  const backendUrl = `http://localhost:8000/api/v1/auth/${endpoint}`;

  try {
    const authHeader = request.headers.get('authorization');

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        ...(authHeader ? { 'authorization': authHeader } : {}),
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy DELETE error:', error);
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}