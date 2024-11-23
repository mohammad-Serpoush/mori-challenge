import React, { useState } from 'react';
import ProductList from '../components/ProductList';
import Search from '../components/Search';
import { getAllProductsByFullText, getAllProductsBySemantic } from '../services/api'; // Import your CRUD functions
import '../styles/HomePage.css';
import ReactLoading from 'react-loading';

function HomePage() {
  const [productsBySemantic, setProductsBySemantic] = useState([]);
  const [productsByFullText, setProductsByFullText] = useState([]);

  const [query, setQuery] = useState("")
  const [availability, setAvailability] = useState({ "label": "All", "value": "" })
  const [category, setCategory] = useState({
    "label": "All",
    "value": "",
  })
  const [minPrice, setMinPrice] = useState()
  const [maxPrice, setMaxPrice] = useState()

  const [loading, setLoading] = useState(false)

  const fetchProducts = async (queryParams) => {
    console.log(queryParams)
    setLoading(true)
    try {
      const productsDataBySemantic = await getAllProductsBySemantic(queryParams);
      const productsDataByFullText = await getAllProductsByFullText(queryParams);
      setProductsBySemantic(productsDataBySemantic);
      setProductsByFullText(productsDataByFullText);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
    setLoading(false)

  };

  const onSearchClick = () => {
    let queryParams = 'query=' + query
    if (availability.value) {
      queryParams = queryParams + "&status=" + "IN_STOCK"
    }
    if (category) {
      queryParams = queryParams + "&category_name=" + category.value

    }
    if (minPrice) {
      queryParams = queryParams + "&min_price=" + minPrice

    }
    if (maxPrice) {
      queryParams = queryParams + "&max_price=" + maxPrice

    }

    fetchProducts(queryParams)
  };


  return (
    <div className="home-page">
      <Search
        query={query}
        setQuery={setQuery}
        onSearchClick={onSearchClick}
        category={category}
        setCategory={setCategory}
        availability={availability}
        setAvailability={setAvailability}
        minPrice={minPrice}
        setMinPrice={setMinPrice}
        maxPrice={maxPrice}
        setMaxPrice={setMaxPrice}
      />
      {loading ?
        <div
          style={{
            display: "flex",
            justifyContent: "center"
          }}
        >
          <ReactLoading type={"bubbles"} color={"#F0C1E1"} height={667} width={375} />
        </div>
        : <>
          <ProductList products={productsBySemantic} />
          <br />
          <h6>---------------------------------------------------</h6>
          <br />
          <ProductList products={productsByFullText} />
        </>
      }
    </div>
  );
}

export default HomePage;
