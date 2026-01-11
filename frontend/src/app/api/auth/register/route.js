import { NextResponse } from 'next/server';

export async function POST(request) {
  console.log('=== PROXY REGISTER ROUTE CALLED ==='); // Debug log

  // Construct the backend URL
  const backendUrl = 'http://localhost:8000/api/v1/auth/register';

  try {
    // Handle FormData (for register which uses FormData)
    const formData = await request.formData();

    console.log('Forwarding request to:', backendUrl); // Debug log

    const response = await fetch(backendUrl, {
      method: 'POST',
      body: formData, // Send the FormData directly
    });

    console.log('Backend response status:', response.status); // Debug log

    const data = await response.json();

    console.log('Backend response data:', data); // Debug log

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Backend request failed', details: error.message }, { status: 500 });
  }
}