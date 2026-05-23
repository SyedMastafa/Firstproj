import React, { useState, useEffect } from 'react';

export default function PriceTracker() {
  const [products, setProducts] = useState([]);

  // ডাটাবেস থেকে ডাটা ফেচ করা (ধরে নিচ্ছি একটি API আছে)
  useEffect(() => {
    fetch('/api/get-prices')
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-5">
      <h1 className="text-3xl font-bold text-center mb-10">BD Tech Price Tracker</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map(product => (
          <div key={product.id} className="bg-white p-4 rounded-lg shadow-md">
            <img src={product.image} alt={product.name} className="h-40 mx-auto" />
            <h2 className="text-xl font-semibold mt-2">{product.name}</h2>
            <p className="text-green-600 font-bold text-lg">৳ {product.price}</p>
            <a href={product.affiliateLink} target="_blank" className="block mt-4 bg-blue-600 text-white text-center py-2 rounded">
              সেরা দামে কিনুন
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}
