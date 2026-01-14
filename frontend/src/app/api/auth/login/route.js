import { NextResponse } from 'next/server';

export async function POST(request) {
  // Construct the backend URL
  const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000/api/v1/auth/login';

  try {
    // Handle FormData (for login which uses FormData)
    const formData = await request.formData();

    console.log('Forwarding login request to:', backendUrl); // Debug log

    const response = await fetch(backendUrl, {
      method: 'POST',
      body: formData, // Send the FormData directly
    });

    console.log('Backend login response status:', response.status); // Debug log

    const data = await response.json();

    console.log('Backend login response data:', data); // Debug log

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy login error:', error);
    return NextResponse.json({ error: 'Backend login request failed', details: error.message }, { status: 500 });
  }
}