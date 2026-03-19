const API_BASE_URL = 'http://localhost:8000';

export async function embedImage(file, secret) {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('secret', secret);

  const response = await fetch(`${API_BASE_URL}/embed`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to embed message');
  }

  const blob = await response.blob();
  const key = response.headers.get('X-Secret-Key');
  return { blob, key };
}

export async function extractMessage(file, key) {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('key', key);

  const response = await fetch(`${API_BASE_URL}/extract`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to extract message');
  }

  return await response.json();
}
