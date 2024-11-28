const Card = ({ title, value, additionalInfo }) => {
    return (
      <div className="card">
       <strong> <p className="value">{value}</p></strong>
        <h3 className="title">{title}</h3>
        
        {additionalInfo && <p>{additionalInfo}</p>}
      </div>
    );
  };
  
  export default Card;
  