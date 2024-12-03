const Card = ({ title, value, additionalInfo, cornerElement }) => {
    return (
      <div className="card">
       {cornerElement && (
        <div className="corner-element">
          <p className="value"> <strong>{value}</strong></p>
          <img src={cornerElement} alt="Corner Icon" className="corner-image" />
        </div>
      )}
       
        <h3 className="title">{title}</h3>
        {additionalInfo && <p>{additionalInfo}</p>}
      </div>
    );
  };
  
  export default Card;
  