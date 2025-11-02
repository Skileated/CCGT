import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { GraphData } from '../api';

interface GraphVizProps {
  graph: GraphData;
}

export default function GraphViz({ graph }: GraphVizProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !graph.nodes.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 600;
    const height = 400;
    svg.attr('width', width).attr('height', height);

    // Create force simulation
    const simulation = d3
      .forceSimulation(graph.nodes as any)
      .force(
        'link',
        d3
          .forceLink(graph.edges)
          .id((d: any) => d.id)
          .distance((d: any) => 150 - d.weight * 100)
      )
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    // Create edges
    const link = svg
      .append('g')
      .selectAll('line')
      .data(graph.edges)
      .enter()
      .append('line')
      .attr('stroke', (d: any) => {
        // Color based on weight and whether it's a disruption
        if (d.reason) return '#ef4444'; // Red for disruptions
        return d.weight > 0.7 ? '#10b981' : d.weight > 0.4 ? '#f59e0b' : '#ef4444';
      })
      .attr('stroke-width', (d: any) => Math.max(1, d.weight * 3))
      .attr('stroke-opacity', 0.6);

    // Create nodes
    const node = svg
      .append('g')
      .selectAll('circle')
      .data(graph.nodes)
      .enter()
      .append('circle')
      .attr('r', (d: any) => 8 + (d.importance_score || 0.5) * 8)
      .attr('fill', (d: any) => {
        const importance = d.importance_score || 0.5;
        return d3.interpolateBlues(importance);
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .call(
        d3
          .drag<any, any>()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    // Add labels
    const label = svg
      .append('g')
      .selectAll('text')
      .data(graph.nodes)
      .enter()
      .append('text')
      .text((d: any) => `S${d.id + 1}`)
      .attr('font-size', '10px')
      .attr('dx', 12)
      .attr('dy', 4)
      .attr('fill', '#374151');

    // Tooltip
    const tooltip = d3
      .select('body')
      .append('div')
      .style('position', 'absolute')
      .style('padding', '8px')
      .style('background', 'rgba(0, 0, 0, 0.8)')
      .style('color', 'white')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0)
      .style('z-index', 1000);

    node
      .on('mouseover', (event, d: any) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip
          .html(
            `<strong>Sentence ${d.id + 1}</strong><br/>${d.text_snippet}<br/>Entropy: ${d.entropy?.toFixed(3) || 'N/A'}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 10 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(200).style('opacity', 0);
      });

    link
      .on('mouseover', (event, d: any) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip
          .html(
            `Weight: ${d.weight.toFixed(3)}<br/>${d.discourse_marker ? `Discourse: ${d.discourse_marker}<br/>` : ''}${d.reason || ''}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 10 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(200).style('opacity', 0);
      });

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);

      label.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y);
    });

    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup
    return () => {
      simulation.stop();
      tooltip.remove();
    };
  }, [graph]);

  return (
    <div className="w-full overflow-auto">
      <svg ref={svgRef} className="w-full border border-gray-200 rounded"></svg>
      <div className="mt-4 text-sm text-gray-600">
        <p>• Drag nodes to rearrange</p>
        <p>• Hover over nodes/edges for details</p>
        <p>• Red edges indicate disruptions</p>
      </div>
    </div>
  );
}

