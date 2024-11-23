import React from 'react';
import ProductCard from './ProductCard';
import '../styles/ProductList.css';

function ProductList({ products }) {

    return (
        <div className="product-list">
            {products.map((product) => (
                <ProductCard
                    key={product._id}
                    product={product}
                />
            ))}
        </div>
    );
}

export default ProductList;