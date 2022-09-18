using Dapper;
using EP_AcademicMicroservice.Entities;
using EP_AcademicMicroservice.Repository;
using System;
using System.Collections.Generic;
using System.Composition;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
namespace EP_AcademicMicroservice.Infraestructure
{
	[Export(typeof(IAcdCampusRepository))]	public class AcdCampusRepository : BaseRepository, IAcdCampusRepository
	{
		#region Constructor
		[ImportingConstructor]
		public AcdCampusRepository(IConnectionFactory cn) : base(cn)
		{

		}
		#endregion

		#region Public Methods
		public Int InsertAcdCampus(AcdCampusEntity item)
		{
			int afect = 0;
			Int Resultado = 0;
			var query = "AcdCampus_Insert";
			var param = new DynamicParameters();

			param.Add(@nAcdCampusCodigo, item.nAcdCampusCodigo, DbType.Int32, direction: ParameterDirection.Output); 
			param.Add(@cPerJurCodigo, item.cPerJurCodigo, DbType.String); 
			param.Add(@cAcdCamDescripcion, item.cAcdCamDescripcion, DbType.String); 
			param.Add(@cAcdCamDescCorta, item.cAcdCamDescCorta, DbType.String); 
			param.Add(@nAcdKeyReferencia, item.nAcdKeyReferencia, DbType.Int32); 
			param.Add(@cAcdKeyReferencia, item.cAcdKeyReferencia, DbType.String); 
			param.Add(@cAcdCamUbiGeo, item.cAcdCamUbiGeo, DbType.String); 
			param.Add(@nAcdCamUbiGeo, item.nAcdCamUbiGeo, DbType.Int32); 
			param.Add(@cAcdCamDireccion, item.cAcdCamDireccion, DbType.String); 
			param.Add(@cAcdCamPersonaResponsable, item.cAcdCamPersonaResponsable, DbType.String); 
			param.Add(@nAcdCamEstado, item.nAcdCamEstado, DbType.Int32); 
			param.Add(@dAcdCamFechaRegistro, item.dAcdCamFechaRegistro, DbType.DateTime); 
			param.Add(@cAcdCamUsuRegistro, item.cAcdCamUsuRegistro, DbType.String); 
			param.Add(@cAcdCamHostRegistro, item.cAcdCamHostRegistro, DbType.String); 

			afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);

			Resultado = param.Get<Int>("@nAcdCampusCodigo");

			return Resultado;
		}


		public bool UpdateAcdCampus(AcdCampusEntity item)
		{
			bool result = true;
			int afect = 0;
			var query = "AcdCampus_Update";
			var param = new DynamicParameters();

			param.Add(@cPerJurCodigo, item.cPerJurCodigo, DbType.String); 
			param.Add(@cAcdCamDescripcion, item.cAcdCamDescripcion, DbType.String); 
			param.Add(@cAcdCamDescCorta, item.cAcdCamDescCorta, DbType.String); 
			param.Add(@nAcdKeyReferencia, item.nAcdKeyReferencia, DbType.Int32); 
			param.Add(@cAcdKeyReferencia, item.cAcdKeyReferencia, DbType.String); 
			param.Add(@cAcdCamUbiGeo, item.cAcdCamUbiGeo, DbType.String); 
			param.Add(@nAcdCamUbiGeo, item.nAcdCamUbiGeo, DbType.Int32); 
			param.Add(@cAcdCamDireccion, item.cAcdCamDireccion, DbType.String); 
			param.Add(@cAcdCamPersonaResponsable, item.cAcdCamPersonaResponsable, DbType.String); 
			param.Add(@nAcdCamEstado, item.nAcdCamEstado, DbType.Int32); 
			param.Add(@dAcdCamFechaUpdate, item.dAcdCamFechaUpdate, DbType.DateTime); 
			param.Add(@cAcdCamUsuarioUpd, item.cAcdCamUsuarioUpd, DbType.String); 
			param.Add(@cAcdCamHostUpd, item.cAcdCamHostUpd, DbType.String); 

			afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);

			return result
		}


		public bool DeleteAcdCampus(DbType.Int32 Id)
		{
			bool exito = false;
			var afect = 0;
			var query = "AcdCampus_Delete";
			var param = new DynamicParameters();

			param.Add("@nAcdCampusCodigo", Id, DbType.Int32);
			afect = SqlMapper.Execute(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);
			exito = afect > 0;

			return exito
		}


		public AcdCampusEntity GetItemAcdCampus(AcdCampusFilter filter, AcdCampusFilterItemType filterType)
		{
			AcdCampusEntity ItemFound = null;
			switch (filterType)
			{
				case AcdCampusFilterItemType.ById:
					ItemFound = this.GetById(filter.nAcdCampusCodigo);
					break;
			}
			return ItemFound;
		}


		public IEnumerable<AcdCampusEntity> GetLstItemAcdCampus(AcdCampusFilter filter, AcdCampusFilterLstItemType filterType, Pagination pagination)
		{
			IEnumerable<AcdCampusEntity> lstItemFound = new List<AcdCampusEntity>();
			switch (filterType)
			{
				case AcdCampusFilterLstItemType.ByPagination:
					lstItemFound = this.GetByPagination();
					break;
				default:
					break;
			}
			return lstItemFound;
		}


		public bool Update(AcdCampusEntity item)
		{
			throw new NotImplementedException();
		}

		public bool Delete(long id)
		{
			throw new NotImplementedException();
		}

		public bool Delete(string id)
		{
			throw new NotImplementedException();
		}


		#endregion

		#region Private Methods Item
		private AcdCampusEntity GetById(DbType.Int32 Id)
		{
			AcdCampusEntity itemFound = null;
			var query ="AcdCampus_Get";
			var param = new DynamicParameters();
			param.Add("@nAcdCampusCodigo", Id, DbType.Int32);
			itemFound = SqlMapper.QueryFirstOrDefault<AcdCampusEntity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);

			return itemFound;
		}


		private IEnumerable<AcdCampusEntity> GetByPagination()
		{
			IEnumerable<AcdCampusEntity> lstFound = new List<AcdCampusEntity>();
			var query ="AcdCampus_Get";
			var param = new DynamicParameters();
			param.Add("@nAcdCampusCodigo", 0, DbType.Int32);
			lstFound = SqlMapper.QueryAcdCampusEntity>(this._connectionFactory.GetConnection, query, param, commandType: CommandType.StoredProcedure);

			return lstFound;
		}

		#endregion
	}
}