using EP_AcademicMicroservice.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace EP_AcademicMicroservice.Repository
{

	public interface IAcdCampusRepository : IGenericRepository<AcdCampusEntity>
	{
		int InsertAcdCampus(AcdCampusEntity item);
		bool UpdateAcdCampus(AcdCampusEntity item);
		bool DeleteAcdCampus(int Id);
		AcdCampusEntity GetItemAcdCampus(AcdCampusFilter filter, AcdCampusFilterItemType filterType);
		IEnumerable<AcdCampusEntity> GetLstItemAcdCampus(AcdCampusFilter filter, AcdCampusFilterLstItemType filterType, Pagination pagination);
	}
}