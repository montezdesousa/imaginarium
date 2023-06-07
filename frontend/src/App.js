import './App.css'
import React, { useState, useEffect, useCallback } from "react";

function isValidHttpUrl(string) {
  let url;
  console.log(string);
  try {
    url = new URL(string);
  } catch (_) {
    console.log(_);
    return false;  
  }

  return url.protocol === "http:" || url.protocol === "https:";
}

const App = () => {
  const [img, setImg] = useState("");
  const [res, setRes] = useState([]);

  const fetchRequest = useCallback(
    async () => {
      const query = document.URL.split("?q=")[1];
      query ? setImg(decodeURIComponent(query)) : setImg("");
      const data = await fetch(`https://backend-nwwimnpnpa-nw.a.run.app/search?q=${query}`);
      const dataJ = await data.json();
      const result = dataJ.results;
      setRes(result);
    },
    []
  );
  
  useEffect(() => {
      fetchRequest();
    }, 
    [fetchRequest]
  );

  return (
    <>
      <div className="row">
        <div className="nav-bar">
          <div className="nav-bar__title">
            <a href="/">
              Imaginarium
            </a>
          </div>
        </div>
        <div className="column-left">        
          <div className="search">
            <div className="search-bar">
              <form className="search-bar__form">
                <input
                  className="search-bar__form__input"
                  type="text"
                  placeholder="Colar link da imagem..."
                  name="q"
                />
                <button
                className="search-bar__form__button"
                  type="submit"
                />
              </form>
            </div>
            <div className="query__container">
              {img && isValidHttpUrl(img) ? (           
                  <>
                    <img
                      className="query__img"
                      src={img}
                      alt="" />
                    <div className="query__overlay"
                      onClick={() => {
                        window.open(img);
                      } } />
                  </>
              ) : (
                <></>
              )}
            </div>
          </div>
          <div className="video">
            {img === "" ?  (           
              <iframe
                className="video__iframe"
                src="https://youtube.com/embed/dwebaxpzBGo"
                title="YouTube video player"
                frameBorder="0"
              />
            ) : (
              <></>
            )}
          </div>
        </div>
        {img !== "" ? (
          <div className="column-right">
            <div className="results">
              <div className="results__title">
                {img && res.length === 0 ? (
                <div className="spinner">
                  <div className="bounce1"></div>
                  <div className="bounce2"></div>
                  <div className="bounce3"></div>
                </div>                ) : (
                  <></>
                )}
              </div>
              <div className="results__images">
                {res.map((val) => {
                  return (
                    <div className="results__container">
                      <div className="results__overlay" onClick={() => {
                          window.open(val.urls.page);
                        }}>
                        {val.title}
                      </div>
                      <img
                        key={val.id}
                        className="results__img"
                        src={val.urls.img}
                        alt=""
                        onClick={() => {
                          window.open(val.urls.page);
                        }}
                      />
                    </div> 
                  );
                })}
              </div>
            </div>
          </div>
        ) : (
          <></>
        )}
      </div>
    </>
  );
};
export default App;
