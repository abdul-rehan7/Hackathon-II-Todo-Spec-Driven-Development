// frontend/src/app/api/proxy/route.js
import { NextResponse } from 'next/server';

export async function POST(request, { params }) {
  const { path } = params; // This would be the dynamic segment
  const body = await request.json();
  const method = request.method;

  // For auth endpoints, construct the backend URL
  const backendUrl = `http://localhost:8000/api/v1/auth/${path}`;

  try {
    const response = await fetch(backendUrl, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(request.headers.entries()),
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}

export async function GET(request, { params }) {
  const { path } = params;
  const backendUrl = `http://localhost:8000/api/v1/auth/${path}`;

  try {
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        ...Object.fromEntries(request.headers.entries()),
      },
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json({ error: 'Backend request failed' }, { status: 500 });
  }
}