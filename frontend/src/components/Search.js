import React, { useEffect, useState } from 'react';
import '../styles/Search.css';

import Select from 'react-select';


function Search({ 
    query, setQuery, onSearchClick, category, setCategory, availability, setAvailability ,minPrice , setMinPrice , maxPrice , setMaxPrice

}) {
    const [options, setOptions] = useState([])
    const categories = ["", 'raincoats', 'sweaters', 'shoes', 'keychains', 'blouses', 'scrunchies', 'waistcoats', 'dresses', 'necklaces', 'hats', 'tops', 'earrings', 'shirts', 'coats', 'shorts', 'ties', 'kimonos', 'headbands', 'sunglasses', 'sweatshirts', 'scarves', 'hoodies', 'bags', 'blazers', 'jackets', 'rings', 'watches', 't-shirts', 'pants', 'bracelets', 'belts', 'skirts', 'anklets', 'socks']

    const availabilityOptions = [
        {
            "label": "In Stock",
            "value": "In Stock",
        },
        {
            "label": "All",
            "value": "",
        },
    ]
    useEffect(() => {
        let options = categories.map((e, i) => {
            if (e == "") {
                return { "label": "All", "value": e }

            }
            return { "label": e, "value": e }
        }
        )
        setOptions(options)


    }, [])
    return (
        <>
            <div style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            }}>
                <input
                    className='search-input'
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button
                    className='search-button'
                    onClick={onSearchClick}
                >Search</button>
            </div>
            <div
                style={{
                    display: "flex",
                    justifyContent: "space-around"
                }}
            >
                <div>
                    <p>Category</p>
                    <Select
                        placeholder={"category"}
                        value={category}
                        onChange={(v) => setCategory(v)}
                        options={options}
                        className='select-box'
                    />
                </div>
                <div>
                    <p>Status</p>
                    <Select
                        placeholder={"Availability"}
                        value={availability}
                        onChange={(v) => setAvailability(v)}
                        options={availabilityOptions}
                        className='select-box'
                    />
                </div>
                <div>
                    <p>Minimum Price</p>

                    <input
                        className='price-input'
                        value={minPrice}
                        onChange={(e) => setMinPrice(e.target.value)}
                    />
                </div>
                <div>
                    <p>Maximum Price</p>

                    <input
                        className='price-input'
                        value={maxPrice}
                        onChange={(e) => setMaxPrice(e.target.value)}
                    />
                </div>
            </div>
        </>
    );
}

export default Search;
