using System;
using System.Threading.Tasks;
using System.Web.Services.Description;
using Microsoft.Owin;
using Owin;
using TrashLocalizationWebsite2.Models;
using System.Collections.Generic;
using System.Linq;
using Microsoft.Extensions.DependencyInjection;


namespace TrashLocalizationWebsite2
{
    public class Startup1
    {
        public void Configuration(IAppBuilder app)
        {
            // For more information on how to configure your application, visit https://go.microsoft.com/fwlink/?LinkID=316888
        }
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddDbContext<BotesEntities1>(options =>
                options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
            services.AddMvcCore();
        }
    }
}
