import React from 'react';
import '../styles/ProductCard.css';

function ProductCard({ product }) {
  return (
    <div className="product-card">
      <div className="product-image">
        <img src={product.images[0]} alt={product.title} />
      </div>
      <div className="product-details">
        <h3>{product.title}</h3>
        {/* <p>{product.description}</p> */}
        <p>${product.price}</p>
      </div>
    </div>
  );
}

export default ProductCard;
